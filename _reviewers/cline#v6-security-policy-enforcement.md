---
title: Security policy enforcement
description: Do not treat “ignore” or best-effort filtering as security. If you must
  prevent unsafe tool access, enforce authorization with policy that the untrusted
  party can’t modify, and implement strict permission checks.
repository: cline/cline#v6
label: Security
language: Other
comments_count: 4
repository_stars: 70864
---

Do not treat “ignore” or best-effort filtering as security. If you must prevent unsafe tool access, enforce authorization with policy that the untrusted party can’t modify, and implement strict permission checks.

**Standards**
1. **Ignore files are not authorization**: If the system can still read files via explicit mentions or shell commands, ignore files must be documented/used only as filtering of irrelevant content—not as access control.
2. **Enforce via trusted hooks/policy**: Use a hook (e.g., `PreToolUse`) to cancel/deny disallowed tool calls. Ensure the enforcement policy comes from a trusted location (e.g., global hooks), not from repository/PR-controlled paths that an attacker can alter.
3. **Validate tool-request shape**: Before approving any action, validate `request.input` structure and types.
4. **Use exact allowlists (and match whole commands)**: Approve only explicitly allowed commands with strict matching, not prefix/substring checks.
5. **Scope by trust**: For tools like Git, document that “safe” behavior depends on whether the repository is trusted; avoid claims that flags make it safe in untrusted repos.

**Example (deny/allow run_commands with strict checks)**
```ts
const cline = await ClineCore.create({
  clientName: "smart-approval",
  capabilities: {
    requestToolApproval: async (request) => {
      const input = request.input as { commands?: unknown; files?: unknown };

      // Only approve exact, known-safe read-only commands.
      if (request.toolName === "run_commands" && Array.isArray(input.commands)) {
        const allowed = new Set([
          "ls",
          "git status",
          "git log --oneline -20",
          "git diff --name-only"
        ]);

        const ok = input.commands.every(
          (cmd) => typeof cmd === "string" && allowed.has(cmd.trim())
        );

        return { approved: ok };
      }

      return { approved: false };
    }
  }
});
```

**Operational guidance**
- When using hooks to block commands, prefer global/trusted hooks. Do not rely on repo-local `.cline/hooks/` or `.clinerules/hooks/` for security decisions, because the same PR can change those files after checkout.