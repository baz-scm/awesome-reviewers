---
title: Secure Tool Controls
description: Do not rely on bypassable or untrusted-code-controlled mechanisms to
  provide security. Enforce tool/command policy at a trusted boundary, validate tool
  inputs, and use strict allowlists (with clear “trusted environment only” assumptions).
repository: cline/cline#v13
label: Security
language: Other
comments_count: 3
repository_stars: 70874
---

Do not rely on bypassable or untrusted-code-controlled mechanisms to provide security. Enforce tool/command policy at a trusted boundary, validate tool inputs, and use strict allowlists (with clear “trusted environment only” assumptions).

Apply:
- Don’t treat repo-provided hooks as security. If a PR/workspace is untrusted, a malicious change can alter/delete the enforcement hook. Use trusted, global hooks/config instead.
- Validate the shape of tool inputs before approving/denying.
- Prefer allowlists over “safe command” heuristics; avoid assuming a command is safe with flags in an untrusted repository.
- If a hook only improves quality (e.g., filtering irrelevant outputs), frame it as filtering—not as a security guarantee.

Example (input-shape validation + strict allowlist):
```ts
const cline = await ClineCore.create({
  clientName: "example",
  capabilities: {
    requestToolApproval: async (request) => {
      const input = request.input as { commands?: unknown; files?: unknown };

      // Only approve an exact allowlist in trusted contexts.
      if (request.toolName === "run_commands" && Array.isArray(input.commands)) {
        const allowed = new Set([
          "ls",
          "git status",
          "git diff --no-ext-diff --no-textconv" // only if you truly trust repo behavior
        ]);

        if (input.commands.every(c => typeof c === "string" && allowed.has(c.trim()))) {
          return { approved: true };
        }
      }

      return { approved: false };
    }
  }
});
```

Enforcement placement rule (high level): Put the blocking/approval logic in global/trusted configuration (e.g., a global PreToolUse hook), not in hooks shipped by the checked-out PR/workspace.