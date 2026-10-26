---
title: Trusted Hook Enforcement
description: 'Treat file ignore/filter mechanisms and repo-provided hooks as *non-security*
  controls: they’re bypassable by the model/user calling tools directly (e.g., explicitly
  reading files) or by having repository content change what gets executed. For real
  security outcomes, enforce at the tool-execution decision point using trusted policy.'
repository: cline/cline#v11
label: Security
language: Other
comments_count: 4
repository_stars: 70871
---

Treat file ignore/filter mechanisms and repo-provided hooks as *non-security* controls: they’re bypassable by the model/user calling tools directly (e.g., explicitly reading files) or by having repository content change what gets executed. For real security outcomes, enforce at the tool-execution decision point using trusted policy.

Apply this standard:
- Don’t document or rely on “ignore” files as an access-control boundary.
- If you need to block tools (e.g., shell commands), enforce it with a trusted `PreToolUse` hook that cancels disallowed calls.
- Do not rely on hooks shipped inside the checked-out repository (`.cline/hooks/`, `.clinerules/hooks/`), because that code can be modified by an attacker.
- When auto-approving tools, validate the exact tool input shape and use strict allowlists for *specific* permitted command strings; avoid assuming “Git is safe” or that flags make complex tools benign.

Example (trusted global enforcement via `PreToolUse` cancel):
```bash
# ~/.cline/hooks/PreToolUse.sh
# Cancels run_commands unless explicitly allowed.
# stdin: JSON event; stdout can be used per your hook framework.

input=$(cat)
# Pseudocode: parse JSON and decide
# if event indicates run_commands and commands are not strictly allowed -> cancel

if echo "$input" | grep -q '"name":"run_commands"'; then
  # Extract commands list and validate exact strings (no permissive prefix matching)
  # If not allowed: exit with a non-zero status / output a stop signal per your hook API.
  exit 1
fi
```

Net effect: security policy lives in a trusted place and is evaluated against validated inputs immediately before tool execution—rather than being treated as “blocking” by hints like ignore files or untrusted repository configuration.