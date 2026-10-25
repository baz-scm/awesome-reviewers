---
title: Trusted Enforcement Overreach
description: Treat hooks/allowlists as *defense-in-depth*, not a primary security
  boundary. Enforce security decisions in a trusted, immutable context, validate inputs
  strictly, and never depend on code coming from an untrusted repository.
repository: CLINE/cline
label: Security
language: Other
comments_count: 4
repository_stars: 70839
---

Treat hooks/allowlists as *defense-in-depth*, not a primary security boundary. Enforce security decisions in a trusted, immutable context, validate inputs strictly, and never depend on code coming from an untrusted repository.

Apply this rule:
- **Don’t rely on repository-provided hooks for blocking.** After a PR/branch is checked out, the PR can change `.cline/hooks/` or `.clinerules/hooks/`. Put blocking logic in the job/workflow environment (e.g., global hook outside the checkout) and/or rely on platform/job permissions.
- **Don’t frame hook behavior as “security”.** If hook implementations can be bypassed or are “too easy to defeat”, present them as **filtering** (e.g., block irrelevant outputs/files) rather than access control.
- **Use strict allowlists with input-shape validation.** Approve only well-defined, whole-command matches from a fixed set, and verify the tool request input has the expected structure before evaluating it. Avoid assuming complex tools become safe via flags in untrusted contexts.
- **Protect generated configuration/secrets.** Anything written to the workspace from remote/org configuration may contain sensitive keys—ensure it’s excluded from commits (e.g., recursive `.gitignore` patterns).

Example (strict tool auto-approval):
```ts
const cline = await ClineCore.create({
  clientName: "smart-approval",
  capabilities: {
    requestToolApproval: async (request) => {
      // Validate expected input structure
      const input = request.input as { commands?: unknown; files?: unknown };

      // Approve only exact whole commands from a fixed allowlist
      const safe = new Set([
        "ls",
        "git status",
        "git diff --oneline --stat", // example: choose only truly read-only forms
        "git log --oneline -20",
      ]);

      if (request.toolName === "run_commands" && Array.isArray(input.commands)) {
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

When you need a hard boundary, use workflow/job permissions or a trusted global enforcement point—not a hook stored in the repository—and keep allowlist logic strict and well-validated.