---
title: Secure Hook Enforcement
description: 'When using hooks/plugins for security-related controls, apply a strict
  trust model and robust enforcement:


  - **Don’t rely on repository-provided hooks/config for blocking** when the repo/PR
  can be changed by an attacker. If the workflow checks out the PR, any `.cline/hooks/`
  (or `.clinerules/hooks/`) it contains should be treated as **untrusted**—it may...'
repository: cline/cline#v27
label: Security
language: Other
comments_count: 4
repository_stars: 70892
---

When using hooks/plugins for security-related controls, apply a strict trust model and robust enforcement:

- **Don’t rely on repository-provided hooks/config for blocking** when the repo/PR can be changed by an attacker. If the workflow checks out the PR, any `.cline/hooks/` (or `.clinerules/hooks/`) it contains should be treated as **untrusted**—it may run with sensitive job environment (e.g., tokens). Enforce allow/deny using **global/admin-controlled** hooks or after removing repo-controlled hook/plugin directories.

- **Validate and constrain tool requests** before approving anything. Approval logic must inspect the tool input’s shape and use **exact-match allowlists** (not “startsWith” or loosely parsed strings). Also assume command safety can depend on untrusted context (e.g., a Git command can execute programs in an untrusted repository even if it looks read-only).

- **Avoid framing easily bypassed hooks as security boundaries.** If your hook can be defeated (e.g., by changing command shape or event differences), treat it as data hygiene/filtering, not a guarantee.

- **Prevent secret leakage from generated workspace config.** Any cached/remote settings directories written into the workspace may contain access keys; add **recursive** `.gitignore` patterns so nested folders are also ignored.

Example pattern for enforcement (conceptual):
```sh
# Global/admin-controlled PreToolUse hook (stored outside the PR workspace)
# Goal: deny run_commands unless the request matches a strict allowlist.
# - Parse the JSON from stdin
# - Validate the expected fields and types
# - Exact-match allowlist; otherwise cancel
#
# If your framework supports it, return a structured “cancel”/“stop” response.
```