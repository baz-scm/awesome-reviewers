---
title: Trust Boundaries For Access
description: When deciding what a model/tool is allowed to do, treat “filters” (ignore
  files, repository-provided hooks) as untrusted and potentially bypassable. Only
  enforce access controls at a trusted boundary, using validated inputs and least-privilege
  credentials.
repository: cline/cline#v15
label: Security
language: Other
comments_count: 5
repository_stars: 70877
---

When deciding what a model/tool is allowed to do, treat “filters” (ignore files, repository-provided hooks) as untrusted and potentially bypassable. Only enforce access controls at a trusted boundary, using validated inputs and least-privilege credentials.

Apply this standard:
- Don’t claim security from bypassable mechanisms. If users/code can still exfiltrate (e.g., by explicitly reading files), the control is not an authorization boundary.
- Never rely on hooks/plugins that come from untrusted code (e.g., PR checkouts). If the job checks out the PR, that PR can modify `.cline`, `.clinerules`, hooks, or plugins before your enforcement runs.
- Validate tool/permission inputs by shape (types/fields) before applying policies; don’t use brittle “safe command” string lists or “safe flags” unless you fully trust the repository and can reason about tool side effects.
- Use least-privilege workflow/credentials, and place cancellation/allow-deny logic in a trusted, global location (applied after removing any repo-controlled `.cline*` directories).
- Treat generated configuration that may contain secrets (e.g., cached remote config/settings) as sensitive and ensure it is gitignored.

Example (trusted hook + input-shape validation):
```ts
// In a trusted PreToolUse hook/plugin (not from a PR checkout)
// Pseudocode for canceling disallowed tool calls by validating request shape.

function onPreToolUse(event) {
  const req = event.input;
  const toolName = event.toolName;

  // Validate structure before policy decisions
  if (toolName === 'run_commands' && Array.isArray(req?.commands)) {
    const allowed = new Set(['ls', 'git status']);

    // If you don’t fully trust the repository, prefer refusing rather than
    // trying to make “safe command flags”.
    const allAllowed = req.commands.every(
      (cmd) => typeof cmd === 'string' && allowed.has(cmd.trim())
    );

    if (!allAllowed) return { stopTask: true };
  }
}
```

Checklist for reviews:
- Is the enforcement point trusted (runs outside repo-controlled artifacts)?
- Can the policy be bypassed by explicit access (reads/cats/commands)?
- Are tool/permission inputs validated by type/shape?
- Are allowlists safe under the stated trust assumptions (or do you refuse when trust is missing)?
- Are any generated settings/config files that may contain keys properly gitignored?