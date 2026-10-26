---
title: Secure Hook Enforcement
description: 'Treat hooks, plugins, and repo-provided scripts as *behavior modifiers*,
  not as your primary security/authorization boundary.


  Apply these rules:


  1) Don’t rely on untrusted repo hooks for enforcement'
repository: cline/cline#v26
label: Security
language: Other
comments_count: 4
repository_stars: 70893
---

Treat hooks, plugins, and repo-provided scripts as *behavior modifiers*, not as your primary security/authorization boundary.

Apply these rules:

1) Don’t rely on untrusted repo hooks for enforcement
- If a workflow/checkout includes pull request code, that code can alter `.cline/hooks/` (or plugins/rules) before execution.
- Enforce allow/deny decisions via workflow/job permissions and trusted locations (global hooks owned by the system, admin/organization controls, or remote config), not via repository contents.

2) Assume hook-based controls can be bypassed
- Even when a hook appears to “stop” something, hook execution can be incomplete, misframed, or otherwise circumvented.
- Use hooks for non-security filtering/cleanup (e.g., removing irrelevant files) rather than for guarantees about safety.

3) When authorizing tool execution, validate and allowlist strictly
- Validate the *shape* of tool inputs before making decisions.
- Approve only an exact allowlisted set; avoid permissive matching.

Example (strict tool authorization with input-shape validation):

```ts
const cline = await ClineCore.create({
  clientName: "smart-approval",
  capabilities: {
    requestToolApproval: (request) => {
      // Validate expected input shape first
      const input = request.input as { commands?: unknown; files?: unknown };

      // Only approve a fixed set of read-only commands (exact match)
      const safeCommands = new Set([
        "ls",
        "git status",
        "git diff --oneline -20",
        "git log --oneline -20",
      ]);

      if (request.toolName === "run_commands" && Array.isArray(input.commands)) {
        const allSafe = input.commands.every(
          (cmd) => typeof cmd === "string" && safeCommands.has(cmd.trim())
        );
        return allSafe ? { approved: true } : { approved: false };
      }

      return { approved: false };
    },
  },
});
```

4) Treat workspace-written configuration/state as sensitive
- If your system writes organization settings, cached rules, or credentials into the workspace, ensure those paths are gitignored with patterns that cover nested folders.

Outcome: security-critical decisions remain enforced by trusted policy layers, while hooks/plugins remain best-effort helpers—not the source of truth for authorization.