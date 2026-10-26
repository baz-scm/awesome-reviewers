---
title: Trusted Tool Authorization
description: 'Security-related constraints should be enforced by trusted authorization
  logic—not by best-effort content filtering that can be bypassed.


  Apply this standard:'
repository: cline/cline#v10
label: Security
language: Other
comments_count: 5
repository_stars: 70869
---

Security-related constraints should be enforced by trusted authorization logic—not by best-effort content filtering that can be bypassed.

Apply this standard:
1) Treat “ignore” files and repo-provided hooks as *non-authoritative*.
   - Don’t describe them as security controls; they can be defeated by direct reads/mentions or changed by the attacker who controls the repo.
2) Enforce allow/deny decisions using trusted context (e.g., admin/workflow-controlled configuration).
   - Prefer global/admin hooks over repository hooks for blocking tool calls.
   - Use CI/job permissions to limit credentials; don’t rely on code checked out from untrusted PRs.
3) Validate tool inputs and use strict allowlisting.
   - Check the exact input shape and match whole commands (including rejecting “almost safe” assumptions).
   - Assume “read-only” tools may execute programs via their own plumbing (e.g., Git in untrusted repos).

Example (strict allowlist + input shape validation):
```ts
const cline = await ClineCore.create({
  clientName: "smart-approval",
  capabilities: {
    requestToolApproval: async (request) => {
      const input = request.input as { commands?: unknown; files?: unknown };

      // Example: allow only exact, known-safe commands in trusted environments.
      if (request.toolName === "run_commands" && Array.isArray(input.commands)) {
        const safe = new Set(["ls", "git status", "git log --oneline -20"]);
        const ok = input.commands.every(
          (cmd) => typeof cmd === "string" && safe.has(cmd.trim())
        );
        return ok ? { approved: true } : { approved: false };
      }

      return { approved: false };
    },
  },
});
```

Also: treat cached enterprise/remote configuration as sensitive and ensure it’s not committed (e.g., correct .gitignore patterns for nested working directories).