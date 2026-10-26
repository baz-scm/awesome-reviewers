---
title: Trust Boundary Permissioning
description: Treat any hook/plugin/script files that come from the workspace (including
  a PR checkout) as untrusted. Enforce security decisions using allowlists and input
  validation, and be precise about what hooks can (and cannot) guarantee.
repository: cline/cline?x=1
label: Security
language: Other
comments_count: 4
repository_stars: 70861
---

Treat any hook/plugin/script files that come from the workspace (including a PR checkout) as untrusted. Enforce security decisions using allowlists and input validation, and be precise about what hooks can (and cannot) guarantee.

Apply this standard:
- Don’t rely on repository-provided hooks/plugins to block dangerous actions. If you use hooks to cancel/deny tool calls, place them in a global location the untrusted code cannot modify.
- Validate tool permission inputs before deciding. Check the exact expected shape/types, and approve only strict, known-safe values (prefer exact-match allowlists).
- Don’t assume “read-only” commands are safe in untrusted repositories. Example: Git may run external programs via repository configuration; only approve such commands when the repository is trusted (or avoid approving them).
- Avoid framing bypassable mechanisms (like simplistic hooks) as security guarantees; describe them as filtering/guardrails within a controlled threat model.
- If your security/authorization model writes cached enterprise/config data into the workspace, ensure it’s gitignored (nested folders too) to prevent leaking secrets.

Example (deny unapproved tool calls via a global PreToolUse hook, not a repo checkout):
```bash
# ~/.cline/hooks/PreToolUse  (global; NOT inside the checked-out PR)
# Cancel run_commands unless explicitly allowed
# (Parse stdin JSON, inspect toolName + input, then exit non-zero or emit a cancel response.)
```