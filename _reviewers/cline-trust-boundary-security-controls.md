---
title: Trust-boundary Security Controls
description: 'Treat “ignore/filter” and heuristics as non-security: they must not
  be relied on for authorization or access control.


  Apply explicit, trusted enforcement instead:'
repository: CLINE/CLINE
label: Security
language: Other
comments_count: 5
repository_stars: 70837
---

Treat “ignore/filter” and heuristics as non-security: they must not be relied on for authorization or access control.

Apply explicit, trusted enforcement instead:
- **Do not use ignore files as a security boundary.** If a model can still request or read files via other means (e.g., tool calls like `cat`), the mechanism is at best a best-effort filter.
- **Use allowlists with strict input validation for tool permissions.** Validate the tool input shape before checking contents, and approve only exact, known-safe commands (avoid assumptions that flags make inherently dangerous tools safe).
- **Respect trust boundaries for hooks/plugins.** In CI/workflows, **do not rely on hooks/plugins from the checked-out repository**, because the PR can modify them. Prefer centrally configured/global enforcement (e.g., user- or runner-level hooks) or perform enforcement before untrusted code is introduced.
- **Account for product/surface enforcement differences.** If some products enforce a control and others don’t, document and design accordingly.
- **Handle security-sensitive configuration safely.** Do not commit cached/generated security configuration that may include secrets; add them to `.gitignore`.

Example (tool permission allowlist + input-shape validation):
```ts
const input = request.input as { commands?: unknown };

// Approve only exact read-only commands (examples):
const safe = new Set([
  "ls",
  "git status",
  "git diff",
  "git log --oneline -20",
]);

if (request.toolName === "run_commands" && Array.isArray(input.commands)) {
  const ok = input.commands.every(
    (cmd) => typeof cmd === "string" && safe.has(cmd.trim())
  );
  if (ok) return { approved: true };
}

return { approved: false };
```

Net effect: security decisions become explicit, testable, and placed at the correct trust boundary—rather than depending on bypassable filters or repository-controlled scripts.