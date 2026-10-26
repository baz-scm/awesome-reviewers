---
title: Secure tool execution
description: 'When automation can execute tools/commands, treat *all* inputs from
  the model and from checked-out repository content as untrusted, then enforce security
  at the right boundaries:'
repository: cline/cline#v2
label: Security
language: Other
comments_count: 3
repository_stars: 70861
---

When automation can execute tools/commands, treat *all* inputs from the model and from checked-out repository content as untrusted, then enforce security at the right boundaries:

- **Validate input shape before applying policy** (avoid brittle parsing/prefix checks). Example pattern:
  ```ts
  const input = request.input as { commands?: unknown };
  if (request.toolName === "run_commands" && Array.isArray(input.commands)) {
    const safe = new Set(["ls", "git status", "git diff --oneline -20", "git log --oneline -20"]);
    if (input.commands.every(c => typeof c === "string" && safe.has(c.trim()))) {
      return { approved: true };
    }
  }
  ```
- **Use strict allowlists of exact safe actions**; don’t rely on string-prefix “safety” (e.g., `cmd.startsWith(...)`).
- **Don’t assume complex tools are safe via flags in untrusted repos** (e.g., Git may execute programs depending on repo config).
- **Enforce authorization outside attacker-controlled repo hooks/config**: if the job checks out the PR, the PR can modify any repo-local hooks/plugins. Require deny/approval via **global hooks loaded before checkout**, or **remove/sanitize** `.cline/` and `.clinerules/` before loading hooks.
- **Prevent sensitive workspace leakage**: if you write remote/enterprise config into the working directory and it can include secrets/keys, ensure **recursive** `.gitignore` rules cover nested folders (so subfolder checkouts can’t accidentally commit secrets).