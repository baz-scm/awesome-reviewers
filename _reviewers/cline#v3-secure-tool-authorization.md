---
title: Secure Tool Authorization
description: 'Treat any “tool execution” (e.g., `run_commands`) as a security boundary:
  do not auto-run commands using weak checks, do not allow repository-controlled code
  to bypass enforcement, and do not leak sensitive generated configuration.'
repository: cline/cline#v3
label: Security
language: Other
comments_count: 3
repository_stars: 70863
---

Treat any “tool execution” (e.g., `run_commands`) as a security boundary: do not auto-run commands using weak checks, do not allow repository-controlled code to bypass enforcement, and do not leak sensitive generated configuration.

Apply this checklist:
- Validate tool input shape before decisions (don’t assume fields/types).
- Use strict allowlists with exact/whole-command matching—avoid naive prefix checks. Treat complex commands (notably Git) as unsafe in untrusted repositories.
- Enforce deny/approval via trusted, globally applied policy (e.g., a trusted `PreToolUse` hook). Do not rely on hooks/plugins from the checked-out PR/repo, since an attacker can modify them.
- Treat generated workspace config as sensitive; add correct `.gitignore` rules that match nested paths.

Example (safe allowlist-style approval):
```ts
requestToolApproval: async (request) => {
  const input = request.input as { commands?: unknown }

  const isRunCommands = request.toolName === "run_commands"
  const commands = input.commands

  if (!isRunCommands || !Array.isArray(commands)) return { approved: false }

  // Allow exact, known-safe commands only.
  const safe = new Set([
    "ls",
    "git status",
    "git diff --oneline --stat",
  ])

  const ok = commands.every(cmd => typeof cmd === "string" && safe.has(cmd.trim()))
  return { approved: ok }
}
```

Example (secret/config hygiene):
```text
**/.cline/enterprise/
**/.cline/remote-config/
```