---
title: Real security enforcement
description: 'Treat “filters” and “repo-local controls” as *not* security boundaries
  unless they are robustly enforced against bypasses.


  Apply these rules:

  1) **Enforce with trusted controls**: If you need to block tool access, do it via
  a control the untrusted code (repo/PR) cannot change (e.g., a globally configured
  hook or pre-checks before loading PR content). Don’t...'
repository: cline/cline#x
label: Security
language: Other
comments_count: 5
repository_stars: 70861
---

Treat “filters” and “repo-local controls” as *not* security boundaries unless they are robustly enforced against bypasses.

Apply these rules:
1) **Enforce with trusted controls**: If you need to block tool access, do it via a control the untrusted code (repo/PR) cannot change (e.g., a globally configured hook or pre-checks before loading PR content). Don’t rely on `.cline/hooks/` checked out from the PR.
2) **Don’t assume ignore files prevent access**: Ignored/filtered items can still be reached through explicit tool input (e.g., shell reads). If you can’t guarantee enforcement, label it as “filtering relevance,” not security.
3) **Validate tool inputs before approving/denying**: Check the *shape* of tool input and allow only a strict set of known-safe commands/options. Never assume flags make inherently dangerous commands safe in untrusted repositories.
4) **Mark generated config as secrets**: Remote/enterprise settings caches may include credentials/access keys—exclude them with recursive `.gitignore` patterns.

Example (allowlisting with shape validation):
```ts
// request.input is untrusted: validate shape before deciding.
const input = request.input as { commands?: unknown; files?: unknown };

if (request.toolName === "run_commands" && Array.isArray(input.commands)) {
  const safeCommands = new Set([
    "ls",
    "git status",
    "git diff --oneline -20",
  ]);

  const approved = input.commands.every(
    (cmd) => typeof cmd === "string" && safeCommands.has(cmd.trim())
  );

  return approved ? { approved: true } : { approved: false };
}

return { approved: false };
```
Operational checklist:
- Prefer a globally controlled `PreToolUse` policy for blocking.
- If documentation/examples could be bypassed, reframe them as non-security filtering or redesign them to be truly enforceable.
- Add secret-like caches to `.gitignore` (e.g., `.cline/enterprise/` and `.cline/remote-config/` with recursive patterns).