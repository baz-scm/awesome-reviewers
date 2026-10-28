---
title: Protect secrets from untrusted code
description: Treat any boundary between untrusted input/code and privileged secrets
  or security controls as a hard trust boundary, and be explicit and honest about
  what a mitigation actually guarantees.
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Security
language: Other
comments_count: 3
repository_stars: 70986
---

Treat any boundary between untrusted input/code and privileged secrets or security controls as a hard trust boundary, and be explicit and honest about what a mitigation actually guarantees.

- Never let code or config originating from untrusted sources (e.g., a checked-out pull request branch) run with access to privileged credentials. In CI/CD, if a job checks out a PR, assume any `.cline/hooks/`, `.clinerules/hooks/`, or `.cline/plugins/` in that checkout can execute attacker-controlled code with the job's full environment (including tokens like `GH_TOKEN`). Mitigate this by checking out the base branch and reading diffs via `gh pr diff`, or by deleting `.cline`/`.clinerules` before running untrusted-adjacent steps, before relying on a global hook as a secondary control.
- When caching or writing sensitive data to the workspace (API keys, access tokens, config secrets), ensure it is excluded from version control with recursive, path-independent ignore patterns (`**/.cline/enterprise/`, not just `.cline/enterprise/`), since a user or CI job may operate from a nested subfolder where root-anchored patterns fail to match. Verify with `git check-ignore` against nested paths.
- Do not label a mechanism as a "security" feature if it can be trivially bypassed (e.g., a model-facing hook that filters file access but has no enforcement teeth). Either make the control actually enforceable, or document it honestly as a convenience/filtering feature rather than a security boundary, so users don't rely on it for protection it can't provide.

Example of a safer CI step instead of trusting PR-checkout hooks:
```yaml
# Avoid checking out the PR head when running Cline with secrets
- run: git checkout main
- run: gh pr diff "$PR_NUMBER" > diff.patch
- run: cline --auto-approve true 'Review diff.patch for issues'
```