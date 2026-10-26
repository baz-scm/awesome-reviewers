---
title: Trusted Tool Authorization
description: Treat file filters (e.g., “ignore”) and repo-provided hooks as *best-effort
  context reduction*, not security boundaries. If a model/tool must be prevented from
  accessing or executing something, enforce that restriction from a trusted control
  plane, and restrict tool execution with strict allowlists.
repository: cline/cline#v9
label: Security
language: Other
comments_count: 4
repository_stars: 70868
---

Treat file filters (e.g., “ignore”) and repo-provided hooks as *best-effort context reduction*, not security boundaries. If a model/tool must be prevented from accessing or executing something, enforce that restriction from a trusted control plane, and restrict tool execution with strict allowlists.

Apply these rules:
1) **No security claims for ignore/filters**: If users can cause the model to read via other channels (explicit mentions, shell commands, etc.), the filter is not authorization.
2) **Do not trust repo-supplied enforcement code**: Anything checked out from an untrusted PR can be modified to bypass your controls. Prefer global/CI-side hooks or server-side policies.
3) **Allowlist tool operations with input validation**: Validate the tool input *shape* before approving, and only approve exact, known-safe commands/arguments. Don’t assume “read-only” commands are safe in untrusted repositories (e.g., Git can execute programs via repo config).
4) **Assume the workspace may contain secrets**: Ensure any generated policy/config artifacts that may include sensitive data are not accidentally committed.

Example (allowlist + input-shape validation):
```ts
// Example permission gating for a tool that runs shell commands.
function canApproveRunCommands(request: {
  toolName: string;
  input: unknown;
}): { approved: boolean } {
  const input = request.input as { commands?: unknown };

  const safe = new Set([
    // Only exact, known-safe commands.
    'ls',
    'git status',
  ]);

  if (request.toolName !== 'run_commands' || !Array.isArray(input.commands)) {
    return { approved: false };
  }

  const allSafe = input.commands.every(
    (cmd) => typeof cmd === 'string' && safe.has(cmd.trim())
  );

  return { approved: allSafe };
}
```

And for command blocking via hooks:
- Use a **trusted global hook** location (CI runner/global config), not a hook inside the checked-out repository, since the PR author can change or remove it.