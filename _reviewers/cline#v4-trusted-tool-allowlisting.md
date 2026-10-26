---
title: Trusted tool allowlisting
description: Do not treat “ignore/filter” mechanisms (like .clineignore) as security
  boundaries. If you need to prevent access or command execution, enforce it with
  trusted, cancelable controls (global/system-side hooks) plus strict validation/allowlisting
  of tool inputs.
repository: cline/cline#v4
label: Security
language: Other
comments_count: 4
repository_stars: 70864
---

Do not treat “ignore/filter” mechanisms (like .clineignore) as security boundaries. If you need to prevent access or command execution, enforce it with trusted, cancelable controls (global/system-side hooks) plus strict validation/allowlisting of tool inputs.

Apply this when documenting or implementing controls:
- **Reframe accurately**: filtering reduces irrelevant data, but the model can still read files via explicit mentions/commands.
- **Don’t trust repo-provided enforcement**: hooks/plugins inside a checked-out PR/workspace can be modified by the attacker; enforce via **global hooks** (or delete/disable repo hook dirs before running).
- **Validate and allowlist tool inputs**: treat `request.input` (or equivalent) as untrusted; check its shape and only approve exact, known-safe operations. Be wary that “safe by flags” is usually false in untrusted repos.

Example (global `PreToolUse` hook concept):
```bash
#!/usr/bin/env bash
# Receives JSON on stdin; cancels disallowed tool calls.
# Pseudocode—implement in your chosen hook runtime.

read -r JSON
HOOK_NAME=$(echo "$JSON" | jq -r '.hookName')
TOOL_NAME=$(echo "$JSON" | jq -r '.preToolUse.toolName // .tool_call.name')
INPUT=$(echo "$JSON" | jq -r '(.preToolUse.parameters // .tool_call.input)')

if [ "$TOOL_NAME" = "run_commands" ]; then
  # Allow only an explicit fixed set of exact read-only commands.
  # If input shape is unexpected, deny/cancel.
  CMDS=$(echo "$JSON" | jq -c '.preToolUse.parameters.commands? // .tool_call.input.commands?')
  if [ "$CMDS" = "null" ]; then
    echo "{\"cancel\":true}"; exit 0
  fi

  # Deny unless every command is in the allowlist.
  if echo "$CMDS" | jq -e 'all(.[]; type=="string" and (IN(.[]; ["ls","git status","git log --oneline -20"])))' >/dev/null; then
    exit 0
  else
    echo "{\"cancel\":true}"; exit 0
  fi
fi

exit 0
```

Documentation standard: state what the control *can* do (reduce accidental access; block certain tool calls) and what it *cannot* guarantee (not true access control over arbitrary file reads by the model).