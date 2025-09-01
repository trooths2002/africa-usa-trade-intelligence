#!/usr/bin/env python3
"""
Lightweight MCP orchestrator for GitHub Actions.

- Maintains a single issue as the 'MCP Task Queue' that contains current tasks and status.
- Checks deployed health endpoint (if reachable) and writes summary into the task queue.
- If unhealthy, creates a clearly labeled issue requesting human or automated agent attention.
- Agents read the task-queue issue to know what to do next; they can add comments when work is done.
This script uses only the repository token (GITHUB_TOKEN), so you don't need additional secrets.
"""
import os
import sys
import time
import requests
from datetime import datetime
from github import Github

REPO_FULL = os.environ.get("GITHUB_REPOSITORY")  # e.g. owner/repo
TOKEN = os.environ.get("GITHUB_TOKEN")
DEPLOYED_URL = os.environ.get("DEPLOYED_URL", "https://africa-usa-trade-intelligence.onrender.com")
TASK_ISSUE_TITLE = "MCP Orchestrator - Task Queue"

if not TOKEN or not REPO_FULL:
    print("GITHUB_TOKEN or GITHUB_REPOSITORY not set. Exiting.")
    sys.exit(1)

gh = Github(TOKEN)
repo = gh.get_repo(REPO_FULL)

def get_or_create_task_issue():
    issues = repo.get_issues(state="open")
    for issue in issues:
        if issue.title.strip() == TASK_ISSUE_TITLE:
            return issue
    # not found -> create
    body = (
        "This issue is the MCP Orchestrator Task Queue.\n\n"
        "Agents and automated workflows should read this issue for the current tasks, "
        "post progress as comments, and open PRs for changes. The orchestrator updates "
        "this issue every 15 minutes with the latest system status.\n\n"
        "Template:\n\n"
        "- [ ] Health check\n"
        "- [ ] Run CI and tests\n"
        "- [ ] Apply auto-fixes (format/lint)\n"
        "- [ ] Validate dashboard connectivity\n\n"
        "Do not close this issue; use comments and PRs for work.\n"
    )
    return repo.create_issue(title=TASK_ISSUE_TITLE, body=body, labels=["mcp-orchestrator"])

def check_deployed_health():
    url = DEPLOYED_URL.rstrip("/") + "/health"
    try:
        r = requests.get(url, timeout=10)
        return {"ok": r.status_code == 200, "status_code": r.status_code, "body": r.text}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def build_status_section():
    now = datetime.utcnow().isoformat() + "Z"
    health = check_deployed_health()
    section = f"## Snapshot @ {now}\n\n"
    if health.get("ok"):
        section += f"- Deployed health: ✅ healthy (HTTP {health['status_code']})\n\n"
    else:
        if "status_code" in health:
            section += f"- Deployed health: ❌ HTTP {health['status_code']}\n\n"
            section += "```\n" + str(health.get("body", "")) + "\n```\n\n"
        else:
            section += f"- Deployed health: ❌ Error - {health.get('error')}\n\n"
    return section

def compose_task_list(existing_body):
    # Conservative: keep original template and append latest status + suggested actions
    status_block = build_status_section()
    suggested_actions = (
        "### Suggested actions for agents\n\n"
        "1. If deployed health is unhealthy:\n"
        "   - Run CI locally / in workflow. Post test failures in a comment.\n"
        "   - If failures are only formatting/linting, create a branch `auto/format-fix-<id>` and open a PR.\n"
        "2. If deployed health is healthy:\n"
        "   - Validate dashboard endpoints and assets.\n"
        "   - Run transitory end-to-end checks (fetch /, /health, sample endpoints).\n"
        "3. Always add a comment to this issue describing actions taken and link PRs.\n\n"
    )
    footer = f"_Updated by MCP Orchestrator at {datetime.utcnow().isoformat()}Z_\n"
    return status_block + suggested_actions + footer

def update_issue(issue):
    new_content = compose_task_list(issue.body or "")
    # Put new content at top while preserving the existing body template below (if present)
    combined = new_content + "\n---\n\n" + (issue.body or "")
    issue.edit(body=combined)
    print("Task queue issue updated.")

def maybe_open_incident(health):
    if not health.get("ok"):
        title = f"[incident] Deployed health failing - {datetime.utcnow().isoformat()}"
        body = (
            "Automated incident created by MCP Orchestrator.\n\n"
            f"Deployed URL: {DEPLOYED_URL}\n\n"
            "Health check details:\n\n"
            "```\n"
            f"{health}\n"
            "```\n\n"
            "Please assign and investigate. Agents may open PRs for safe fixes (formatting/linting) and "
            "attach test results in comments."
        )
        existing = [i for i in repo.get_issues(state="open") if i.title.startswith("[incident] Deployed health failing")]
        if not existing:
            repo.create_issue(title=title, body=body, labels=["incident"])
            print("Incident issue created.")
        else:
            print("Incident issue already present; skipping creation.")
    else:
        print("Health ok — no incident opened.")

def main():
    issue = get_or_create_task_issue()
    health = check_deployed_health()
    update_issue(issue)
    maybe_open_incident(health)
    # Optionally leave a timestamp comment for traceability
    issue.create_comment(f"MCP Orchestrator ran at {datetime.utcnow().isoformat()}Z")
    print("Orchestrator run complete.")

if __name__ == "__main__":
    main()