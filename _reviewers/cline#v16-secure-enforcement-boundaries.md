---
title: Secure enforcement boundaries
description: Do not rely on bypassable “filters” (ignore files, file lists, or other
  content-shaping features) as an access-control/security boundary. If the model can
  still read or act on the underlying content, the control is only UX.
repository: cline/cline#v16
label: Security
language: Other
comments_count: 5
repository_stars: 70882
---

Do not rely on bypassable “filters” (ignore files, file lists, or other content-shaping features) as an access-control/security boundary. If the model can still read or act on the underlying content, the control is only UX.

Instead:
1) Enforce at the point of action (e.g., block/cancel tool calls such as `run_commands`) using trusted, runtime enforcement.
2) Treat repository-controlled configuration as untrusted. If the workflow/agent checks out a PR, the PR can modify `.cline/` hooks/rules—use global hooks or pre-step removal.
3) Implement tool permissions with strict allowlists and input validation. Avoid “safe command flags” heuristics for complex tools (e.g., Git may spawn programs); if you don’t fully trust the repository, don’t auto-approve broad command families.
4) Don’t commit sensitive generated config/caches (e.g., workspace folders containing keys); gitignore them.

Example (CI hook to block disallowed commands):
```sh
# Write a global PreToolUse hook (outside the checked-out PR)
cat > ~/.cline/hooks/PreToolUse <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
event=$(cat)
# Inspect the tool call and cancel if it’s not allowed
# (Implement shape checks + a strict allowlist here.)
if echo "$event" | grep -q '"toolName":"run_commands"'; then
  # reject by default; only allow exact approved commands
  echo "$event" | grep -Eq '"commands"\s*:\s*\["(ls|git status)"\]'
  allowed=$?
  if [ $allowed -ne 0 ]; then
    # cancel the task/run
    echo '{"action":"cancel"}'
    exit 0
  fi
fi
EOF
chmod +x ~/.cline/hooks/PreToolUse
```

Codify these rules in your team standards: “Ignore/filter != security,” “enforce tool access at runtime in trusted scope,” and “allowlist + validate, don’t guess safety from flags.”