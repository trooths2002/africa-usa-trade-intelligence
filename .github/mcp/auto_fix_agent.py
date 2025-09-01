#!/usr/bin/env python3
"""
Automated MCP Agent for applying auto-fixes (formatting, linting, etc.)
This agent reads the MCP Task Queue issue and applies safe fixes automatically.
"""
import os
import sys
import subprocess
import tempfile
from datetime import datetime
from github import Github

REPO_FULL = os.environ.get("GITHUB_REPOSITORY")
TOKEN = os.environ.get("GITHUB_TOKEN")
TASK_ISSUE_TITLE = "MCP Orchestrator - Task Queue"

if not TOKEN or not REPO_FULL:
    print("GITHUB_TOKEN or GITHUB_REPOSITORY not set. Exiting.")
    sys.exit(1)

gh = Github(TOKEN)
repo = gh.get_repo(REPO_FULL)

def get_task_issue():
    """Get the MCP Task Queue issue"""
    issues = repo.get_issues(state="open")
    for issue in issues:
        if issue.title.strip() == TASK_ISSUE_TITLE:
            return issue
    return None

def check_formatting_issues():
    """Check for formatting issues using black"""
    try:
        result = subprocess.run(['black', '--check', '.'], 
                              capture_output=True, text=True, cwd='.')
        return result.returncode != 0, result.stdout, result.stderr
    except FileNotFoundError:
        return False, "", "Black not installed"

def check_linting_issues():
    """Check for linting issues using ruff"""
    try:
        result = subprocess.run(['ruff', 'check', '.'], 
                              capture_output=True, text=True, cwd='.')
        return result.returncode != 0, result.stdout, result.stderr
    except FileNotFoundError:
        return False, "", "Ruff not installed"

def apply_formatting_fixes():
    """Apply formatting fixes using black"""
    try:
        result = subprocess.run(['black', '.'], 
                              capture_output=True, text=True, cwd='.')
        return result.returncode == 0, result.stdout, result.stderr
    except FileNotFoundError:
        return False, "", "Black not installed"

def apply_linting_fixes():
    """Apply linting fixes using ruff"""
    try:
        result = subprocess.run(['ruff', 'check', '--fix', '.'], 
                              capture_output=True, text=True, cwd='.')
        return result.returncode == 0, result.stdout, result.stderr
    except FileNotFoundError:
        return False, "", "Ruff not installed"

def run_tests():
    """Run tests to ensure fixes don't break functionality"""
    try:
        result = subprocess.run(['pytest', 'tests/'], 
                              capture_output=True, text=True, cwd='.')
        return result.returncode == 0, result.stdout, result.stderr
    except FileNotFoundError:
        return False, "", "Pytest not installed"

def create_fix_branch():
    """Create a branch for auto-fixes"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    branch_name = f"auto/format-fix-{timestamp}"
    
    # Get the default branch
    default_branch = repo.default_branch
    
    # Get the commit SHA of the default branch
    base_commit = repo.get_branch(default_branch).commit.sha
    
    # Create a new branch
    repo.create_git_ref(f"refs/heads/{branch_name}", base_commit)
    
    return branch_name

def commit_and_push_fixes(branch_name, commit_message):
    """Commit and push fixes to the branch"""
    try:
        # Add all changes
        subprocess.run(['git', 'add', '.'], check=True, cwd='.')
        
        # Commit changes
        subprocess.run(['git', 'commit', '-m', commit_message], check=True, cwd='.')
        
        # Push to the branch
        subprocess.run(['git', 'push', 'origin', branch_name], check=True, cwd='.')
        
        return True, "Changes committed and pushed successfully"
    except subprocess.CalledProcessError as e:
        return False, f"Failed to commit and push: {e}"

def create_pull_request(branch_name, title, body):
    """Create a pull request for the fixes"""
    try:
        pr = repo.create_pull(
            title=title,
            body=body,
            head=branch_name,
            base=repo.default_branch
        )
        # Add auto-fix label
        pr.add_to_labels("auto-fix")
        return pr
    except Exception as e:
        return None

def main():
    print("MCP Auto-Fix Agent starting...")
    
    # Get the task queue issue
    task_issue = get_task_issue()
    if not task_issue:
        print("Task queue issue not found. Exiting.")
        return
    
    # Check for formatting issues
    print("Checking for formatting issues...")
    has_formatting_issues, format_stdout, format_stderr = check_formatting_issues()
    
    # Check for linting issues
    print("Checking for linting issues...")
    has_linting_issues, lint_stdout, lint_stderr = check_linting_issues()
    
    # If there are no issues, exit
    if not has_formatting_issues and not has_linting_issues:
        print("No formatting or linting issues found.")
        return
    
    # Run tests first to ensure we're starting from a good state
    print("Running tests to verify current state...")
    tests_pass, test_stdout, test_stderr = run_tests()
    
    if not tests_pass:
        print("Tests are failing. Cannot proceed with auto-fixes.")
        # Add a comment to the task issue
        comment = (
            "Auto-fix agent attempted to run but tests are currently failing. "
            "Please fix tests before applying auto-fixes.\n\n"
            "Test output:\n```\n" + test_stdout + test_stderr + "\n```"
        )
        task_issue.create_comment(comment)
        return
    
    # Apply fixes
    print("Applying auto-fixes...")
    
    # Create a branch for the fixes
    branch_name = create_fix_branch()
    print(f"Created branch: {branch_name}")
    
    # Apply formatting fixes
    if has_formatting_issues:
        print("Applying formatting fixes...")
        format_success, format_out, format_err = apply_formatting_fixes()
        if not format_success:
            print(f"Formatting fixes failed: {format_err}")
    
    # Apply linting fixes
    if has_linting_issues:
        print("Applying linting fixes...")
        lint_success, lint_out, lint_err = apply_linting_fixes()
        if not lint_success:
            print(f"Linting fixes failed: {lint_err}")
    
    # Run tests again to ensure fixes don't break anything
    print("Running tests after applying fixes...")
    tests_pass_after, test_stdout_after, test_stderr_after = run_tests()
    
    if not tests_pass_after:
        print("Tests failed after applying fixes. Reverting changes.")
        # Add a comment to the task issue
        comment = (
            "Auto-fix agent applied fixes but tests are now failing. "
            "Changes have been reverted.\n\n"
            "Test output after fixes:\n```\n" + test_stdout_after + test_stderr_after + "\n```"
        )
        task_issue.create_comment(comment)
        return
    
    # Commit and push fixes
    print("Committing and pushing fixes...")
    commit_success, commit_msg = commit_and_push_fixes(
        branch_name, 
        "chore: auto-format & lint fixes (automated)"
    )
    
    if not commit_success:
        print(f"Failed to commit and push: {commit_msg}")
        return
    
    # Create a pull request
    print("Creating pull request...")
    pr_body = (
        "Automated pull request created by MCP Auto-Fix Agent.\n\n"
        "This PR contains automatic formatting and linting fixes.\n\n"
        "Formatting check output:\n```\n" + format_stdout + "\n```\n\n"
        "Linting check output:\n```\n" + lint_stdout + "\n```\n\n"
        "All tests pass after applying these fixes."
    )
    
    pr = create_pull_request(
        branch_name,
        "chore: auto-format & lint fixes (automated)",
        pr_body
    )
    
    if pr:
        # Add a comment to the task issue
        comment = (
            "Auto-fix agent has applied formatting and linting fixes.\n\n"
            f"Pull request created: #{pr.number}\n"
            f"Branch: {branch_name}\n\n"
            "Please review and merge if appropriate."
        )
        task_issue.create_comment(comment)
        print(f"Pull request created: #{pr.number}")
    else:
        print("Failed to create pull request.")

if __name__ == "__main__":
    main()