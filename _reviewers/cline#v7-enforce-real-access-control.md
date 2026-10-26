---
title: Enforce real access control
description: 'Treat “ignore/filters” as *not security*: if a file/config is only used
  to reduce what gets loaded automatically, it must not be relied on to prevent data
  access or command execution. For security, enforce at the tool-execution boundary
  with trusted, validated allow/deny logic, and assume repository-provided hooks/plugins/config
  are untrusted.'
repository: cline/cline#v7
label: Security
language: Other
comments_count: 4
repository_stars: 70865
---

Treat “ignore/filters” as *not security*: if a file/config is only used to reduce what gets loaded automatically, it must not be relied on to prevent data access or command execution. For security, enforce at the tool-execution boundary with trusted, validated allow/deny logic, and assume repository-provided hooks/plugins/config are untrusted.

Apply these rules:
- Don’t rely on ignore/filter mechanisms for access control (they’re bypassable via explicit mentions or direct commands).
- Implement enforcement where commands/tools are about to run (e.g., a `PreToolUse` hook that can cancel the call).
- Keep enforcement outside the untrusted workspace/repo. In CI, prefer a global/user hook; do not rely on `.cline/hooks/` or `.clinerules/hooks/` from the checked-out PR.
- Validate tool request input shape before approving anything; use strict allowlists of exact commands/arguments.
- Make trust-boundary decisions: if a repo is untrusted, avoid assuming complex tools (e.g., Git) can be made safe via flags.

Example (global runtime allowlist via `PreToolUse`):
```sh
# ~/.cline/hooks/PreToolUse.sh (trusted location)
# Cancel disallowed run_commands calls; allow only an exact set.

read -r payload
# payload contains event JSON on stdin

toolName=$(echo "$payload" | node -e 'let s="";process.stdin.on("data",d=>s+=d);process.stdin.on("end",()=>{let j=JSON.parse(s);process.stdout.write(j.hookName||"")});')
# Prefer parsing fully in your real script; this snippet is illustrative.

# In practice, parse JSON and check request.toolName + request.input shape.
# Then: if disallowed, print a response that cancels the task/tool call.
# If allowed, emit whatever your hook protocol expects for “continue”.
```

Standard outcome: security claims should be backed by enforcement that cannot be bypassed by repo-controlled configuration or by the model directly referencing content.