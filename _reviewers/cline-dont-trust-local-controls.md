---
title: Don’t Trust Local Controls
description: 'Treat any “filter” (e.g., file ignores) as *non-security* unless it
  is enforced by a trusted, bypass-resistant control point.


  Apply this standard:

  - **Never rely on ignore lists as an access boundary.** If a mechanism can be bypassed
  by explicit reads/commands, document it as *best-effort filtering* only (or remove
  it).'
repository: Cline/Cline
label: Security
language: Other
comments_count: 5
repository_stars: 70840
---

Treat any “filter” (e.g., file ignores) as *non-security* unless it is enforced by a trusted, bypass-resistant control point.

Apply this standard:
- **Never rely on ignore lists as an access boundary.** If a mechanism can be bypassed by explicit reads/commands, document it as *best-effort filtering* only (or remove it).
- **Enforce tool allow/deny decisions in trusted locations.** In CI/automation, **do not rely on hooks/plugins committed in the PR/repo** (the job checks out the PR, so the attacker can change/delete them). Use **global hooks** (e.g., `~/.cline/hooks/`) or pre-checkout cleanup.
- **Validate tool request shapes before approving.** Don’t do string-prefix checks on raw input; ensure the expected structure/type exists.
- **Avoid “safe flags” assumptions in untrusted repos.** Some tools (notably Git) may execute programs via repo config or flags; only approve commands when you explicitly trust the repository/environment, and narrow the allowlist accordingly.
- **Prevent secret leakage from workspace-written config.** Ensure any remote/org settings written into the workspace are excluded from commits with correct `.gitignore` patterns.

Example (safe-shaped approval only):
```ts
requestToolApproval: async (request) => {
  const input = request.input as { commands?: unknown; files?: unknown };

  // Approve ONLY an explicitly supported, typed allowlist shape
  if (request.toolName === "run_commands" && Array.isArray(input.commands)) {
    const allowed = new Set(["ls", "git status", "git log --oneline -20"]);
    if (input.commands.every(c => typeof c === "string" && allowed.has(c.trim()))) {
      return { approved: true };
    }
  }

  return { approved: false };
}
```

Security outcome: controls become harder to bypass, fewer tool executions slip through due to malformed inputs, and secrets/configuration won’t be accidentally committed.