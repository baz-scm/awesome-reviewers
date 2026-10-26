---
title: Secure Hooks And Allowlisting
description: 'When using hooks/plugins to influence what a task can do, treat extensibility
  as untrusted and enforce security in the host with strict validation.


  Do:'
repository: cline/cline#v14
label: Security
language: Other
comments_count: 4
repository_stars: 70876
---

When using hooks/plugins to influence what a task can do, treat extensibility as untrusted and enforce security in the host with strict validation.

Do:
- **Do not rely on repo-provided hooks/plugins for security decisions.** If the workflow checks out attacker-controlled content, the attacker can modify `.cline/hooks/` or `.clinerules/hooks/` before it runs. Use **global/out-of-repo** controls (or remove/avoid untrusted hook directories before the security decision point).
- **Implement authorization with defensive allowlisting and strict input validation.** Validate the tool input’s structure before applying rules; avoid substring/prefix matches and only approve commands that exactly match an explicit allowlist.
- **Be conservative with complex tools in untrusted environments.** For example, don’t assume Git becomes “safe” via flags—if the repository isn’t trusted, restrict approvals accordingly.
- **If enterprise/remote config writes secret-bearing files into the workspace, ensure they’re never committed.** Use recursive `.gitignore` patterns that cover nested subfolders.

Example (host-side gating pattern):
```ts
// request.input is untrusted model/tool input; validate shape first.
const input = request.input as { commands?: unknown };

const safeCommands = new Set([
  'ls',
  'git status',
  'git diff --oneline -20',
]);

if (request.toolName === 'run_commands' && Array.isArray(input.commands)) {
  const ok = input.commands.every(
    (cmd) => typeof cmd === 'string' && safeCommands.has(cmd.trim())
  );
  if (ok) return { approved: true };
}
return { approved: false };
```

Example (gitignore for secret-bearing cached config):
```gitignore
**/.cline/enterprise/
**/.cline/remote-config/
```