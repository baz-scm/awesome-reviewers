---
title: Harden Hooks and Permissions
description: 'Enforcement logic that attempts to “secure” tool execution via hooks/plugins
  must be treated as security-critical, with clear trust boundaries.


  **Standards**'
repository: cline/cline#v22
label: Security
language: Other
comments_count: 4
repository_stars: 70886
---

Enforcement logic that attempts to “secure” tool execution via hooks/plugins must be treated as security-critical, with clear trust boundaries.

**Standards**
1. **Don’t trust repository-provided hooks/plugins for enforcement.** Treat anything inside a checked-out PR workspace (e.g., `.cline/hooks/`, `.clinerules/hooks/`, plugins within the repo) as attacker-controlled. If you need to block/allow actions, place the enforcing hook/config in a trusted location (e.g., global user hooks), and assume the job’s environment may include sensitive credentials.
2. **Use strict allowlists with input-shape validation for auto-approval.** When approving tool execution, validate the tool input’s structure before making decisions, and only approve a small fixed set of known-safe commands (match whole commands; avoid partial-string checks). Keep examples conservative, especially for commands whose safety depends on repository state.
3. **Don’t market bypassable mitigations as “security.”** If hook-based filtering can be defeated, frame it as reducing noise (e.g., filtering irrelevant targets), not as a guarantee against malicious behavior.
4. **Prevent accidental secret commits from generated config.** Any workspace directories written by remote/enterprise configuration may include sensitive values—ensure they are gitignored with recursive patterns.

**Example: strict tool auto-approval**
```ts
const cline = await ClineCore.create({
  clientName: "smart-approval",
  capabilities: {
    requestToolApproval: async (request) => {
      // Validate the input shape before reasoning about it.
      const input = request.input as { commands?: unknown };

      if (request.toolName === "run_commands" && Array.isArray(input.commands)) {
        // Approve only whole, fixed commands.
        const safeCommands = new Set([
          "ls",
          "git status",
          "git diff --oneline -20",
          "git diff --stat",
          "git log --oneline -20",
        ]);

        const allAllowed = input.commands.every(
          (cmd) => typeof cmd === "string" && safeCommands.has(cmd.trim())
        );

        if (allAllowed) return { approved: true };
      }

      return { approved: false };
    },
  },
});
```

**Practical checklist**
- Enforcement hook lives in a trusted/global location, not in PR content.
- Tool approval logic: validate schema → allowlist → exact matching.
- No “security guarantee” language for bypassable controls; describe as filtering only.
- Generated enterprise/config folders are gitignored (including nested paths).