#!/usr/bin/env python3
"""
Workflow Validation Script
==========================

Validates that all GitHub Actions workflows have correct YAML syntax
and required fields for the branch protection system.
"""

import os
import yaml
from pathlib import Path


def validate_workflow(workflow_path):
    """Validate a single workflow file"""
    try:
        with open(workflow_path, 'r') as f:
            workflow_data = yaml.safe_load(f)
        
        # Basic validation
        if not isinstance(workflow_data, dict):
            return False, "Not a valid YAML dictionary"
        
        if 'name' not in workflow_data:
            return False, "Missing 'name' field"
        
        if 'on' not in workflow_data:
            return False, "Missing 'on' field"
        
        if 'jobs' not in workflow_data:
            return False, "Missing 'jobs' field"
        
        return True, f"Valid workflow: {workflow_data['name']}"
        
    except yaml.YAMLError as e:
        return False, f"YAML syntax error: {e}"
    except Exception as e:
        return False, f"Validation error: {e}"


def main():
    """Main validation function"""
    workflows_dir = Path('.github/workflows')
    
    if not workflows_dir.exists():
        print("❌ .github/workflows directory not found")
        return False
    
    # Find all workflow files
    workflow_files = list(workflows_dir.glob('*.yml')) + list(workflows_dir.glob('*.yaml'))
    
    if not workflow_files:
        print("❌ No workflow files found")
        return False
    
    print(f"🔍 Validating {len(workflow_files)} workflow files...")
    print()
    
    all_valid = True
    
    for workflow_file in sorted(workflow_files):
        is_valid, message = validate_workflow(workflow_file)
        
        if is_valid:
            print(f"✅ {workflow_file.name}: {message}")
        else:
            print(f"❌ {workflow_file.name}: {message}")
            all_valid = False
    
    print()
    
    if all_valid:
        print("🎉 All workflows are valid!")
        
        # Check for required workflows
        required_workflows = {
            'ci.yml': 'CI Pipeline',
            'codeql.yml': 'CodeQL Security Analysis', 
            'e2e-smoke.yml': 'E2E Smoke Tests',
            'observability.yml': 'Observability Monitoring',
            'staged-deployment.yml': 'Staged Deployment',
            'incident-management.yml': 'Incident Management',
            'mcp-auto-fix-agent.yml': 'Auto-Fix Agent'
        }
        
        print()
        print("📋 Checking required workflows for branch protection:")
        
        found_workflows = {f.name for f in workflow_files}
        missing_workflows = []
        
        for required, description in required_workflows.items():
            if required in found_workflows:
                print(f"✅ {required}: {description}")
            else:
                print(f"⚠️  {required}: {description} (MISSING)")
                missing_workflows.append(required)
        
        if missing_workflows:
            print(f"\n⚠️  {len(missing_workflows)} required workflows are missing for complete branch protection")
        else:
            print("\n🎯 All required workflows are present!")
            print("\nNext steps:")
            print("1. Run: python scripts/configure_branch_protection.py --token $GITHUB_TOKEN")
            print("2. Configure required GitHub Secrets")
            print("3. Test with a sample pull request")
        
        return len(missing_workflows) == 0
    else:
        print("❌ Some workflows have validation errors")
        return False


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)