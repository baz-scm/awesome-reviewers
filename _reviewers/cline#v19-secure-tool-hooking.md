---
title: Secure Tool Hooking
description: 'Treat hook/plugin-based controls as part of your security boundary:
  assume any code loaded from a checked-out repository (e.g., `.cline/hooks/`, `.clinerules/hooks/`,
  repo-provided plugins) is untrusted and can be altered by the same attacker you’re
  trying to prevent.'
repository: cline/cline#v19
label: Security
language: Other
comments_count: 4
repository_stars: 70885
---

Treat hook/plugin-based controls as part of your security boundary: assume any code loaded from a checked-out repository (e.g., `.cline/hooks/`, `.clinerules/hooks/`, repo-provided plugins) is untrusted and can be altered by the same attacker you’re trying to prevent.

## Standards
1. **Enforce from trusted locations only**
   - If you need to block tool calls (e.g., `run_commands`), use **global** enforcement (e.g., a user/org-managed `PreToolUse` hook), not repo hooks.
   - Don’t assume “security via hooks in the workspace” works when the workspace can be modified by the PR/job.

2. **Use strict allowlists + validate input shape**
   - Approvals must be based on validated, well-typed input and exact matching of intended commands.
   - Don’t do partial/fragile string matching; reject unknown structures.

3. **Never trust “safe flags” in untrusted repos**
   - If a tool’s behavior depends on repository configuration (e.g., Git smudge/filters, fsmonitor, external diff/conv), only approve those tools in **trusted repositories**.

4. **Prevent secret leakage from generated config**
   - If org/remote configuration is written into the workspace and can include credentials/keys, ensure your `.gitignore` rules cover the correct directories and nested paths.

## Example: strict approval with input validation
```ts
// request.input: raw model tool input; validate shape before approving
const input = request.input as { commands?: unknown; files?: unknown };

if (request.toolName === "run_commands" && Array.isArray(input.commands)) {
  const safe = new Set([
    "ls",
    "git status",
    "git log --oneline -20",
    "git diff" // only if repo is trusted
  ]);

  const allAllowed = input.commands.every(
    (cmd) => typeof cmd === "string" && safe.has(cmd.trim())
  );

  if (allAllowed) return { approved: true };
}

return { approved: false };
```

## Checklist
- [ ] Security decisions don’t rely on repo-provided hooks/plugins.
- [ ] Tool approval logic validates the input schema.
- [ ] Command matching is exact and allowlist-driven.
- [ ] Approving repo-sensitive tools is limited to trusted repos.
- [ ] Workspace-written config that may include secrets is gitignored with nested-path-safe patterns.