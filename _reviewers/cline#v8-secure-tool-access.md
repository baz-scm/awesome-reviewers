---
title: Secure tool access
description: Do not rely on “ignore”/filter mechanisms as security controls—explicit
  reads or tool calls can bypass them. If you need to restrict what the model/tooling
  can do, enforce it with trusted authorization points (e.g., a global `PreToolUse`
  hook), and implement that authorization using (1) input-shape validation and (2)
  strict allowlists, not substring...
repository: cline/cline#v8
label: Security
language: Other
comments_count: 4
repository_stars: 70867
---

Do not rely on “ignore”/filter mechanisms as security controls—explicit reads or tool calls can bypass them. If you need to restrict what the model/tooling can do, enforce it with trusted authorization points (e.g., a global `PreToolUse` hook), and implement that authorization using (1) input-shape validation and (2) strict allowlists, not substring matching or “safe command” assumptions that fail in untrusted repos.

**Practical standard**
1. **No security by `.ignore` / path filtering.** Treat ignored files as still accessible by explicit requests.
2. **Enforce in trusted scope.** Don’t rely on repository-provided hooks/plugins for authorization; a PR can modify them. Use global hooks configured by the job/environment.
3. **Validate tool request inputs.** Before checking permissions, confirm the expected structure and types of `request.input`.
4. **Allowlist exact, known-safe commands.** Match whole commands only; do not infer safety from partial strings or common flags.
5. **Assume contextual risk.** If the command can invoke external programs or repository-controlled hooks (e.g., Git behavior in untrusted repos), don’t treat it as safe.

**Example (trusted `PreToolUse` cancel + strict allowlist)**
```ts
// Pseudocode for a PreToolUse hook that blocks/approves run_commands.
// Principle: validate request.input shape, then allowlist exact commands.

const input = request.input as { commands?: unknown };

if (request.toolName === 'run_commands') {
  if (!Array.isArray(input.commands)) return { approved: false };

  const allowed = new Set([
    'ls',
    'git status',
    'git diff --no-pager',
  ]);

  const allAllowed = input.commands.every(
    (cmd) => typeof cmd === 'string' && allowed.has(cmd.trim())
  );

  return allAllowed ? { approved: true } : { approved: false };
}
```

**Checklist for pull-request/repo workflows**
- Authorization logic lives in CI/job-controlled hooks or config.
- Repo `.cline/hooks/` (or similar) is treated as untrusted input, not an enforcement layer.
- The allowlist is conservative and reviewed whenever you add/modify permitted tools/commands.