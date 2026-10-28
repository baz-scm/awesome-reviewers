---
title: Secure automated command execution
description: When building allowlists, hooks, or auto-approval logic that lets an
  agent or CI job run commands and scripts automatically, assume any boundary that
  can be bypassed by configuration, flags, or untrusted code is not a security control.
repository: cline/cline#|sleep 4
label: Security
language: Other
comments_count: 4
repository_stars: 70979
---

When building allowlists, hooks, or auto-approval logic that lets an agent or CI job run commands and scripts automatically, assume any boundary that can be bypassed by configuration, flags, or untrusted code is not a security control.

- Don't allowlist by command name or prefix alone. Tools like `git` can be reconfigured (`diff.external`, `core.fsmonitor`, etc.) to execute arbitrary programs even for "read-only" commands such as `git diff` or `git status`. Match whole commands against a fixed set, document that this is only safe in repositories you trust, and never assume a flag or subcommand is inherently non-destructive.
- Don't frame easily-defeated filtering (e.g., a hook that just inspects file paths) as a security mechanism. If it can't reliably block a determined actor, describe it as a convenience/filtering feature, not a safety guarantee.
- Treat code checked out from an untrusted source (e.g., a pull request in CI) as hostile: any hooks or plugins it contains will run with the job's environment and secrets (such as `GH_TOKEN`). Don't rely on repo-local hook folders for sandboxing in this scenario — either avoid checking out untrusted refs directly (read diffs via API instead), strip `.cline`/`.clinerules` before the sensitive step, or enforce restrictions via a global/host-level hook that the untrusted code cannot modify.
- When a tool caches sensitive data (API keys, tokens, config) into files inside the workspace, ensure they are excluded from version control with recursive, not root-anchored, `.gitignore` patterns (e.g., `**/.cline/enterprise/` rather than `.cline/enterprise/`), since contributors may work from a subdirectory where a root-anchored pattern won't match.

In short: identify every path by which configuration, environment, or untrusted input could escalate privileges or bypass a control, and design the control (or its documentation) around the real threat model rather than the common case.