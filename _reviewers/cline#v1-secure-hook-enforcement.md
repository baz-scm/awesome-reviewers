---
title: Secure Hook Enforcement
description: Treat hooks/plugins as untrusted (repo-controlled) automation, not a
  security boundary. Enforce authorization/permissions in trusted configuration (job
  `permissions`, global/managed hooks), and never rely on hook code shipped inside
  a checked-out PR/workspace.
repository: cline/cline#v1
label: Security
language: Other
comments_count: 3
repository_stars: 70862
---

Treat hooks/plugins as untrusted (repo-controlled) automation, not a security boundary. Enforce authorization/permissions in trusted configuration (job `permissions`, global/managed hooks), and never rely on hook code shipped inside a checked-out PR/workspace.

Guidelines:
- **Do not rely on repository hooks for security.** If the hook can be modified by an attacker (e.g., lives under checked-out `.cline/hooks/`), it cannot reliably block malicious actions.
- **Validate hook/tool inputs before allowlisting.** Parse the received input shape and only apply allow decisions to exactly-typed, minimal data.
- **Use conservative allowlists in untrusted contexts.** Prefer read-only, whole-command matches; avoid assuming complex tools/flags (e.g., Git) are safe in repositories you don’t trust.
- **Frame hook behavior correctly.** Use hooks for *filtering/cleanup* or reducing noise; don’t present them as a secure mitigation unless enforcement is anchored in trusted control.

Example (trusted global `PreToolUse` hook to block shell commands):
```bash
#!/usr/bin/env bash
set -euo pipefail

echo "{" >/dev/null  # placeholder: read stdin next
payload=$(cat)
# payload includes event info; you must parse it robustly in your real hook
# Pseudocode: if event is run_commands and commands contain anything not in allowlist -> cancel

# In practice, implement this in JS/TS/Python with proper JSON parsing and strict matching.
# Then output a structured response that cancels the tool call.

echo "$payload" | jq -e '
  .hookName == "tool_call" and
  .tool_call.name == "run_commands" and
  ([.tool_call.input.commands[]?] | all(. as $c | $c|test("^(ls|cat|grep)$"))) == true
' >/dev/null
# If allowed, do nothing; if not allowed, emit cancel/deny response per the hook API.
```

If you need a real security control (authorization, blocking, preventing data exfiltration), implement it as a trusted policy (managed configuration / job permissions / globally installed hooks) and treat repo content (including PR-provided hooks or plugins) as untrusted input.