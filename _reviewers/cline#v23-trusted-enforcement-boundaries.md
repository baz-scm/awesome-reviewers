---
title: Trusted Enforcement Boundaries
description: Don’t use user-controlled scripts/hooks or repository-provided files
  as the basis for security decisions. Treat hooks as advisory/filtering unless they
  run from a trusted boundary (e.g., admin/global configuration or a CI job that you
  control).
repository: cline/cline#v23
label: Security
language: Other
comments_count: 3
repository_stars: 70889
---

Don’t use user-controlled scripts/hooks or repository-provided files as the basis for security decisions. Treat hooks as advisory/filtering unless they run from a trusted boundary (e.g., admin/global configuration or a CI job that you control).

Apply these rules:
1) Authorization must be enforced from trusted scope
- Never rely on hooks committed in the target repository (e.g., `.cline/hooks/` or `.clinerules/hooks/`) to block or approve sensitive tool actions. Assume the repository can be modified by an attacker.
- If you need enforcement, use CI/workflow permissions and/or a trusted global hook path/config that the PR cannot change.

2) Validate tool inputs + use strict allowlists
- When auto-approving or permitting tools, validate the request payload shape first.
- Prefer exact match allowlists (exact command strings/parameters). Avoid “broad read-only” assumptions.
- Treat commands like Git as unsafe to approve in untrusted repositories even if they appear read-only; there may be repository-configured hooks/ext drivers that execute programs.

Example (strict allowlist with shape validation for approvals):
```ts
const cline = await ClineCore.create({
  clientName: "secure-approval",
  capabilities: {
    requestToolApproval: async (request) => {
      const input = request.input as { commands?: unknown };

      // Validate shape
      if (request.toolName !== "run_commands" || !Array.isArray(input.commands)) {
        return { approved: false };
      }

      // Exact allowlist only
      const safe = new Set([
        "ls",
        "git status",
        "git log --oneline -20",
      ]);

      const allAllowed = input.commands.every(
        (cmd) => typeof cmd === "string" && safe.has(cmd.trim())
      );

      return { approved: allAllowed };
    }
  }
});
```

3) Frame hook usage correctly
- Use hooks for non-authoritative filtering/sanitization (e.g., hiding irrelevant output), not as the sole security mechanism.
- If you must rely on hooks for blocking, ensure the hook file is sourced from a trusted, non-user-modifiable location and runs with the appropriate environment.

These practices prevent easy-to-bypass “security” that an attacker can defeat by modifying repo content, hook logic, or command parameters.