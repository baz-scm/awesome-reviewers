---
title: Do Not Trust Filters
description: 'Security-critical enforcement must not rely on “filters” or repository-provided
  configuration.


  Apply this standard:

  - Treat ignore lists (e.g., “ignore this file”) as non-security: the model/user
  can still access content via explicit references or tool calls.'
repository: cline/cline#v17
label: Security
language: Other
comments_count: 4
repository_stars: 70883
---

Security-critical enforcement must not rely on “filters” or repository-provided configuration.

Apply this standard:
- Treat ignore lists (e.g., “ignore this file”) as non-security: the model/user can still access content via explicit references or tool calls.
- If you block tool actions, do it with real authorization (deny/allow lists) and robust input validation—not with heuristics that are easy to bypass.
- Never trust hooks/plugins/config that come from the checked-out repository when running with privileged credentials (e.g., tokens). Prefer admin/global enforcement (outside the repo) so the attacker can’t modify the enforcement.
- Be conservative with complex tools: if a “safe” command cannot be proven safe in untrusted repos, deny it rather than trying to guess flags.

Example (strict allowlist + input-shape validation):
```ts
requestToolApproval: async (request) => {
  // Validate shape first
  const input = request.input as { commands?: unknown; files?: unknown };

  // Only auto-approve an exact, minimal set of read-only commands
  const safeCommands = new Set([
    "ls",
    "git status",
    "git diff --oneline -20", // example: prefer exact forms you can reason about
  ]);

  if (request.toolName === "run_commands" && Array.isArray(input.commands)) {
    const ok = input.commands.every(
      (cmd) => typeof cmd === "string" && safeCommands.has(cmd.trim())
    );
    return ok ? { approved: true } : { approved: false };
  }

  return { approved: false };
}
```

Rule of thumb: if the repository (or model output) can change the enforcement mechanism, it’s not a security boundary. Centralize authorization and make it strict enough that bypass-by-structure or bypass-by-flags is not your strategy.