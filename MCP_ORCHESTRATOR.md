# MCP Orchestrator System

## Overview
The MCP Orchestrator is an automated system that continuously monitors the Africa-USA Trade Intelligence Platform and coordinates tasks between human and automated agents. It runs every 15 minutes and maintains a task queue in GitHub Issues to coordinate work.

## How It Works

### 1. Task Queue Issue
The orchestrator maintains a GitHub Issue titled "MCP Orchestrator - Task Queue" that serves as the central coordination point for all agents. This issue contains:
- Current system status
- Suggested actions for agents
- Template for common tasks

### 2. Health Monitoring
Every 15 minutes, the orchestrator checks the health of the deployed system by calling the `/health` endpoint. It reports the status in the task queue issue.

### 3. Incident Management
If the system is unhealthy, the orchestrator automatically creates an incident issue to alert human agents to investigate.

### 4. Agent Coordination
Both human and automated agents can:
- Read the task queue issue to understand current priorities
- Add comments describing work completed
- Open pull requests for fixes
- Update the community on progress

## Agent Instructions

### Where to Look
- Primary coordination: Issue titled "MCP Orchestrator - Task Queue"
- The orchestrator updates that issue periodically with the latest status and suggested actions

### Basic Agent Workflow

1. **Read the latest content** in the task-queue issue
2. **If health is failing**:
   - Run CI (locally or via workflow). Gather pytest output & ruff/black results
   - If fixes are purely formatting/linting:
     - Create a branch named `auto/format-fix-<timestamp>`
     - Apply fixes (`black .`, `ruff check --fix .`)
     - Run tests locally
     - Commit & push, open a PR titled "chore: auto-format & lint fixes (automated)" and add label "auto-fix"
     - Post a comment in the task-queue issue with PR link and test run summary
   - If fixes require code changes beyond lint/format:
     - Create an issue describing root cause, suggested fix, and include reproduction steps
     - If able, create a draft PR and mark it for human review
3. **If health is healthy**:
   - Run end-to-end smoke checks and post results as a comment
4. **Always add a comment** to the task-queue issue describing what you did and link PRs/issues
5. **Respect human reviews** before merging

### Recommended Labels
- `mcp-orchestrator`
- `auto-fix`
- `incident`
- `needs-review`

### Commit Message/Conventional Commits
- `chore: auto-format & lint fixes`
- `fix: correct failing unit test <short>`
- `feat: add monitoring or health checks`

### Security
- Do not request or store secrets in the repo
- Use repository workflows or the GITHUB_TOKEN for authorized actions

## System Components

### Orchestrator Script
Located at `.github/mcp/orchestrator.py`, this script:
1. Checks system health via the `/health` endpoint
2. Maintains the task queue issue
3. Creates incident issues when needed
4. Updates the task queue with current status

### GitHub Actions Workflow
Located at `.github/workflows/mcp-orchestrator.yml`, this workflow:
1. Runs every 15 minutes
2. Sets up Python environment
3. Installs required dependencies
4. Executes the orchestrator script

## Environment Variables

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `GITHUB_TOKEN` | GitHub token for API access | Provided by GitHub Actions |
| `DEPLOYED_URL` | URL of deployed application | https://africa-usa-trade-intelligence.onrender.com |
| `GITHUB_REPOSITORY` | Repository identifier | Provided by GitHub Actions |

## Task Queue Issue Structure

The task queue issue follows this structure:

```
## Snapshot @ <timestamp>
- Deployed health: ✅ healthy (HTTP 200)

### Suggested actions for agents
1. If deployed health is unhealthy:
   - Run CI locally / in workflow. Post test failures in a comment.
   - If failures are only formatting/linting, create a branch `auto/format-fix-<id>` and open a PR.
2. If deployed health is healthy:
   - Validate dashboard endpoints and assets.
   - Run transitory end-to-end checks (fetch /, /health, sample endpoints).
3. Always add a comment to this issue describing actions taken and link PRs.

_Updated by MCP Orchestrator at <timestamp>_

---

This issue is the MCP Orchestrator Task Queue.

Agents and automated workflows should read this issue for the current tasks, 
post progress as comments, and open PRs for changes. The orchestrator updates 
this issue every 15 minutes with the latest system status.

Template:

- [ ] Health check
- [ ] Run CI and tests
- [ ] Apply auto-fixes (format/lint)
- [ ] Validate dashboard connectivity

Do not close this issue; use comments and PRs for work.
```

## Incident Management

When the system health check fails, the orchestrator creates an incident issue with:
- Title: `[incident] Deployed health failing - <timestamp>`
- Description of the health check failure
- Details about the deployed URL
- Labels: `incident`

This ensures that human agents are notified immediately when there are issues with the deployed system.

## Automated Fixes

The orchestrator is designed to work with automated agents that can:
1. Detect issues through the task queue
2. Apply safe fixes (formatting, linting) automatically
3. Open pull requests for human review
4. Post updates to the task queue issue

This creates a self-healing system that can maintain itself with minimal human intervention.