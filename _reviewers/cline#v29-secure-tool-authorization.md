---
title: Secure Tool Authorization
description: Do not rely on “file ignore” or superficial filtering as a security boundary.
  For anything that affects access (which files can be read, which commands can run,
  which secrets are exposed), enforce authorization by cancelling or rewriting tool
  calls in a trusted pre-execution step, using strict allowlists and input-shape validation.
repository: cline/cline#v29
label: Security
language: Other
comments_count: 5
repository_stars: 70893
---

Do not rely on “file ignore” or superficial filtering as a security boundary. For anything that affects access (which files can be read, which commands can run, which secrets are exposed), enforce authorization by cancelling or rewriting tool calls in a trusted pre-execution step, using strict allowlists and input-shape validation.

Apply these rules:
- Treat ignore files/filters (e.g., `.clineignore`) as *non-security UX*; they will be bypassed (e.g., the model can directly read files via explicit commands).
- Implement allowlist-based authorization for tool execution, and validate the raw tool input shape before deciding. Assume “unsafe” tools (e.g., Git) can execute subprocesses depending on repository config—only approve such tools in repositories you trust.
- Put enforcement code in a *trusted location*: do not depend on hooks/plugins shipped in a pull request checkout (attacker can modify them). Prefer global/CI-managed hooks (e.g., `~/.cline/hooks/` on the runner).
- If you need to block, cancel at `PreToolUse` (fail closed for disallowed actions).
- Protect generated config containing sensitive data by ensuring it is not committed (add the relevant runtime folders to `.gitignore`).

Example (global `PreToolUse` hook):
```bash
#!/usr/bin/env bash
set -euo pipefail

# stdin: JSON event
payload=$(cat)
# Example assumes a run tool named run_commands with input.commands as an array of strings.
# Cancel unless every command is exactly in an allowlist.

# (Pseudo-processing; adapt to your environment)
allowed=$(python3 - <<'PY'
import json,sys
p=json.loads(sys.stdin.read())
# Determine tool call shape
name=p.get('preToolUse',{}).get('toolName') or p.get('tool_call',{}).get('name')
inp=p.get('preToolUse',{}).get('parameters') or p.get('tool_call',{}).get('input') or {}
cmds=inp.get('commands')
allow={'ls','git status','git log --oneline -20','git diff --name-only'}
if name!='run_commands' or not isinstance(cmds,list):
    print('DENY');sys.exit(0)
for c in cmds:
    if not isinstance(c,str) or c.strip() not in allow:
        print('DENY');sys.exit(0)
print('ALLOW')
PY
)

if [[ "$allowed" == "DENY" ]]; then
  # Respond to stop/cancel the task/run per your hook contract.
  echo '{"action":"cancel","reason":"run_commands not allowed"}'
  exit 0
fi

echo '{"action":"allow"}'
```
Keep policy in trusted, versioned infrastructure; don’t place “security” logic in repo-controlled files that an attacker can edit.