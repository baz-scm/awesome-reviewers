---
title: Secure Tool Approval
description: 'When your system can execute powerful actions (e.g., shell tools), enforce
  a clear trust boundary and authorization model:


  - Validate the tool input shape before inspecting it.'
repository: cline/cline#v5
label: Security
language: Other
comments_count: 3
repository_stars: 70864
---

When your system can execute powerful actions (e.g., shell tools), enforce a clear trust boundary and authorization model:

- Validate the tool input shape before inspecting it.
- Auto-approve only an explicit allowlist of exact, read-only commands; avoid prefix/substr matching and avoid “trust me” flags for complex tools (e.g., Git behavior can change with repo config).
- Don’t rely on repo-provided hooks/plugins for security enforcement—PR/workspace checkout can let untrusted code run. Prefer controls loaded from a trusted/global location.
- Treat remote configuration/policy artifacts written into the workspace as sensitive and prevent accidental commits with correctly scoped ignore rules.

Example (command allowlisting + input validation):
```ts
const input = request.input as { commands?: unknown };

if (request.toolName === "run_commands" && Array.isArray(input.commands)) {
  const allowed = new Set([
    "ls",
    "git status",
    "git log --oneline -20",
  ]);

  const safe = input.commands.every(
    (cmd) => typeof cmd === "string" && allowed.has(cmd.trim())
  );

  if (safe) return { approved: true };
}

return { approved: false };
```

Example (don’t commit sensitive remote config):
```gitignore
**/.cline/enterprise/
**/.cline/remote-config/
```

This standard prevents untrusted inputs and repo-controlled configuration from turning “automation” into unintended execution or data leakage.