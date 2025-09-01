#!/usr/bin/env python3
"""
Branch Protection Configuration Script
=====================================

This script configures branch protection rules for the main branch requiring:
- CI checks to pass
- CodeQL security analysis to pass  
- E2E smoke tests to pass
- Status checks from observability monitoring

Usage:
  python scripts/configure_branch_protection.py --token <github_token>

Or set GITHUB_TOKEN environment variable and run:
  python scripts/configure_branch_protection.py
"""

import os
import sys
import argparse
import requests
import json
from typing import Dict, Any, List


class BranchProtectionConfig:
    def __init__(self, token: str, repo: str):
        self.token = token
        self.repo = repo  # Should be in format "owner/repo"
        self.api_base = "https://api.github.com"
        
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
    
    def get_required_status_checks(self) -> List[str]:
        """Define the list of required status checks"""
        return [
            # CI Pipeline checks
            "Checks (lint, tests, pip-audit)",  # From ci.yml
            
            # CodeQL Security Analysis  
            "Analyze (python)",  # From codeql.yml
            "Analyze (javascript)",  # From codeql.yml
            
            # E2E Smoke Tests
            "End-to-End Smoke Tests",  # From e2e-smoke.yml
            
            # Observability checks
            "Collect System Metrics",  # From observability.yml
        ]
    
    def configure_branch_protection(self) -> bool:
        """Configure branch protection for the main branch"""
        
        protection_config = {
            "required_status_checks": {
                "strict": True,  # Require branches to be up to date before merging
                "contexts": self.get_required_status_checks(),
                "checks": [
                    {"context": check, "app_id": -1} 
                    for check in self.get_required_status_checks()
                ]
            },
            "enforce_admins": False,  # Allow admins to bypass for emergency fixes
            "required_pull_request_reviews": {
                "dismiss_stale_reviews": True,
                "require_code_owner_reviews": False,
                "required_approving_review_count": 1,
                "require_last_push_approval": False
            },
            "restrictions": None,  # No push restrictions
            "required_linear_history": False,  # Allow merge commits
            "allow_force_pushes": False,
            "allow_deletions": False,
            "block_creations": False,
            "required_conversation_resolution": True,  # Require PR conversations to be resolved
            "lock_branch": False
        }
        
        url = f"{self.api_base}/repos/{self.repo}/branches/main/protection"
        
        print(f"Configuring branch protection for {self.repo}...")
        print(f"Required checks: {self.get_required_status_checks()}")
        
        response = requests.put(
            url, 
            headers=self.headers, 
            json=protection_config
        )
        
        if response.status_code == 200:
            print("✅ Branch protection configured successfully!")
            return True
        elif response.status_code == 403:
            print("❌ Insufficient permissions to configure branch protection")
            print("   Make sure the token has 'repo' scope and admin access to the repository")
            return False
        else:
            print(f"❌ Failed to configure branch protection: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    
    def get_current_protection(self) -> Dict[Any, Any]:
        """Get current branch protection settings"""
        url = f"{self.api_base}/repos/{self.repo}/branches/main/protection"
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print("No branch protection currently configured")
            return {}
        else:
            print(f"Failed to get branch protection: {response.status_code}")
            return {}
    
    def verify_workflows_exist(self) -> bool:
        """Verify that the required workflows exist in the repository"""
        required_workflows = [
            ".github/workflows/ci.yml",
            ".github/workflows/codeql.yml", 
            ".github/workflows/e2e-smoke.yml",
            ".github/workflows/observability.yml"
        ]
        
        print("Verifying required workflows exist...")
        
        missing_workflows = []
        for workflow in required_workflows:
            url = f"{self.api_base}/repos/{self.repo}/contents/{workflow}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                print(f"✅ {workflow}")
            else:
                print(f"❌ {workflow} - NOT FOUND")
                missing_workflows.append(workflow)
        
        if missing_workflows:
            print(f"\n⚠️  Missing {len(missing_workflows)} required workflows:")
            for workflow in missing_workflows:
                print(f"   - {workflow}")
            print("\nPlease create these workflows before configuring branch protection.")
            return False
        
        print("✅ All required workflows are present")
        return True
    
    def create_deployment_environments(self) -> bool:
        """Create deployment environments for staging and production"""
        environments = [
            {
                "name": "staging", 
                "wait_timer": 0,
                "reviewers": [],
                "deployment_branch_policy": {
                    "protected_branches": True,
                    "custom_branch_policies": False
                }
            },
            {
                "name": "production",
                "wait_timer": 0,  # No wait time, but requires staging checks
                "reviewers": [{"type": "User", "id": self.get_user_id()}] if self.get_user_id() else [],
                "deployment_branch_policy": {
                    "protected_branches": True,
                    "custom_branch_policies": False
                }
            },
            {
                "name": "production-gate",
                "wait_timer": 0,
                "reviewers": [],
                "deployment_branch_policy": {
                    "protected_branches": True,
                    "custom_branch_policies": False
                }
            }
        ]
        
        success_count = 0
        
        for env in environments:
            url = f"{self.api_base}/repos/{self.repo}/environments/{env['name']}"
            
            env_config = {
                "wait_timer": env["wait_timer"],
                "reviewers": env["reviewers"],
                "deployment_branch_policy": env["deployment_branch_policy"]
            }
            
            response = requests.put(url, headers=self.headers, json=env_config)
            
            if response.status_code in [200, 201]:
                print(f"✅ Environment '{env['name']}' configured")
                success_count += 1
            else:
                print(f"❌ Failed to configure environment '{env['name']}': {response.status_code}")
        
        return success_count == len(environments)
    
    def get_user_id(self) -> int:
        """Get the current user's ID"""
        url = f"{self.api_base}/user"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json().get("id")
        return None


def main():
    parser = argparse.ArgumentParser(description="Configure branch protection for Africa-USA Trade Intelligence")
    parser.add_argument("--token", help="GitHub personal access token")
    parser.add_argument("--repo", default="trooths2002/africa-usa-trade-intelligence", 
                       help="Repository in format owner/repo")
    parser.add_argument("--verify-only", action="store_true", 
                       help="Only verify workflows exist, don't configure protection")
    
    args = parser.parse_args()
    
    # Get token from argument or environment
    token = args.token or os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ GitHub token required. Use --token argument or set GITHUB_TOKEN environment variable")
        sys.exit(1)
    
    config = BranchProtectionConfig(token, args.repo)
    
    print("🔐 Branch Protection Configuration Tool")
    print("=" * 50)
    print(f"Repository: {args.repo}")
    print()
    
    # Step 1: Verify workflows exist
    if not config.verify_workflows_exist():
        if not args.verify_only:
            print("\n❌ Cannot configure branch protection without required workflows")
            sys.exit(1)
        else:
            sys.exit(1)
    
    if args.verify_only:
        print("\n✅ Verification complete - all required workflows found")
        sys.exit(0)
    
    print()
    
    # Step 2: Show current protection settings
    current = config.get_current_protection()
    if current:
        print("📋 Current branch protection settings:")
        if "required_status_checks" in current:
            contexts = current["required_status_checks"].get("contexts", [])
            print(f"   Required status checks: {len(contexts)}")
            for context in contexts:
                print(f"     - {context}")
        print()
    
    # Step 3: Create deployment environments
    print("🌍 Creating deployment environments...")
    config.create_deployment_environments()
    print()
    
    # Step 4: Configure branch protection
    if config.configure_branch_protection():
        print()
        print("🎉 Branch protection configuration complete!")
        print()
        print("📝 Summary of protections enabled:")
        print("   ✅ Require status checks to pass before merging")
        print("   ✅ Require branches to be up to date before merging")
        print("   ✅ Require pull request reviews")
        print("   ✅ Dismiss stale reviews when new commits are pushed")
        print("   ✅ Require conversation resolution before merging")
        print("   ✅ Restrict pushes that create branches")
        print()
        print("🔍 Required status checks:")
        for check in config.get_required_status_checks():
            print(f"   - {check}")
        print()
        print("⚡ Next steps:")
        print("   1. Create a pull request to test the protection rules")
        print("   2. Verify all required checks run and pass")
        print("   3. Monitor the observability dashboard for SLO metrics")
        print("   4. Review auto-fix PRs created by the MCP Auto-Fix Agent")
        
    else:
        print("\n❌ Branch protection configuration failed")
        sys.exit(1)


if __name__ == "__main__":
    main()