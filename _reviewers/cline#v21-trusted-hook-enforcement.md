---
title: Trusted Hook Enforcement
description: Security controls that depend on hooks/scripts and command approval must
  treat anything coming from the workspace/PR as untrusted, validate inputs strictly,
  and avoid “security-by-hook” marketing.
repository: cline/cline#v21
label: Security
language: Other
comments_count: 3
repository_stars: 70886
---

Security controls that depend on hooks/scripts and command approval must treat anything coming from the workspace/PR as untrusted, validate inputs strictly, and avoid “security-by-hook” marketing.

Apply this standard:
- **Only enforce from trusted sources**: do not rely on hooks/plugins found in a checked-out PR workspace (those can be modified by the PR). Prefer **global hooks** or workflow-controlled configuration after removing/sanitizing the checked-out hooks/plugins and any sensitive context.
- **Assume the model/tool input is untrusted**: validate the *shape* of tool requests before allowlisting.
- **Use strict allowlists with exact matching**: allow only exact command strings you understand; don’t rely on “safe flags” for complex tools (e.g., VCS/Git behavior can vary by repo settings). If you can’t guarantee repository trust, don’t pretend the command is safe.

Example (safe approval pattern):
```ts
// request.input is untrusted; validate its shape first.
const input = request.input as { commands?: unknown; files?: unknown };

if (request.toolName === "run_commands" && Array.isArray(input.commands)) {
  const safeCommands = new Set([
    "ls",
    "git status",
    "git log --oneline -20",
    "git diff" // only if you truly trust the repo behavior
  ]);

  // Exact match (no prefix tricks, no partial/shell interpretation).
  if (input.commands.every(cmd => typeof cmd === "string" && safeCommands.has(cmd.trim()))) {
    return { approved: true };
  }
}
return { approved: false };
```

Checklist:
- [ ] Are you enforcing via a **trusted** path (not `.cline/hooks/` or `.clinerules/hooks/` from a PR checkout)?
- [ ] Are you validating tool request input types/structure before allowlisting?
- [ ] Are you using **exact** allowlists (not prefix/substring checks)?
- [ ] If the repo isn’t trusted, have you avoided pretending “flags make it safe,” and instead reduced privileges / removed untrusted configuration before execution?