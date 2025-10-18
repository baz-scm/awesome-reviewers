---
name: agent-orchestration
description: Coordinate reviewer prompts and repository context to operate Awesome Reviewers as a reusable agent workflow.
license: MIT
allowed-tools:
  - curl
  - jq
metadata:
  primary-reviewer: tokio-guided-code-review
  focus: end-to-end-developer-support
  maturity: production-tested
layout: skill
title: Agent Orchestration Playbook
summary: Build a reusable automation that pulls reviewer prompts, discussion threads, and repo metadata into a single deployment workflow.
---

## When to Load

Use this skill when you need to automate the full Reviewer ingestion workflow for a project or onboarding flow. It packages the highest-signal reviewer prompt with discussion summaries so an agent can reason about context before touching code.

## Inputs

- **Repository slug** (`org/repo`) that already has a reviewer prompt
- Optional branch or commit hash for fetching additional examples
- Shared secrets for deployment automations

## Workflow Overview

1. Fetch the reviewer prompt JSON and Markdown for the target repository.
2. Parse source discussions that back the reviewer prompt to pull out failure modes.
3. Assemble a runbook that agents can replay whenever new pull requests arrive.

```bash
#!/usr/bin/env bash
set -euo pipefail

REVIEWER_SLUG="$1"
BASE_URL="https://awesomereviewers.com/reviewers/${REVIEWER_SLUG}"

curl -fsSL "${BASE_URL}/index.json" \
  | jq '.prompt' \
  > "${REVIEWER_SLUG}-prompt.md"

curl -fsSL "${BASE_URL}/discussions.json" \
  | jq -r '.discussions[] | "### " + .title + "\n" + .summary' \
  > "${REVIEWER_SLUG}-discussions.md"

cat <<'RUNBOOK' > "${REVIEWER_SLUG}-runbook.md"
# ${REVIEWER_SLUG} Runbook

1. Review the prompt file for evaluation heuristics.
2. Scan discussion summaries to anticipate regressions.
3. Draft a plan and ask the agent to execute the reviewer prompt with repo-specific context.
RUNBOOK
```

## Agent Hand-off Script

Deliver this script to the automation layer so the agent knows how to load the skill:

```json
{
  "skill": "agent-orchestration",
  "instructions": [
    "Load the reviewer prompt from {{ reviewer_slug }}",
    "Summarize open discussions for new regressions",
    "Propose deployment steps that align with the recorded runbook"
  ],
  "artifacts": [
    "{{ reviewer_slug }}-prompt.md",
    "{{ reviewer_slug }}-discussions.md",
    "{{ reviewer_slug }}-runbook.md"
  ]
}
```

## Additional Notes

- Rotate access tokens monthly and store them in your agent credential vault.
- Extend the runbook with repository-specific health checks to catch flaky tests.
- Pair this skill with deployment-specific skills when the repo requires bespoke rollout steps.

