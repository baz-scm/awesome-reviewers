---
title: Secure Hook and Command Controls
description: Treat hooks/plugins as guardrails, not a security boundary. Enforce security
  with explicit allowlists and clear trust boundaries, and never allow untrusted parties
  (e.g., a pull request) to supply enforcement code or modify the environment you
  rely on.
repository: cline/cline#v12
label: Security
language: Other
comments_count: 4
repository_stars: 70872
---

Treat hooks/plugins as guardrails, not a security boundary. Enforce security with explicit allowlists and clear trust boundaries, and never allow untrusted parties (e.g., a pull request) to supply enforcement code or modify the environment you rely on.

Apply these rules:
1) **Never rely on repository-provided hooks for enforcement**
   - If the job checks out attacker-controlled code, the PR can change `.cline/hooks/` (and related rule files). Create/insert any enforcement hook from the workflow/admin-controlled side.

2) **Validate tool inputs and match exact allowlists**
   - Don’t do substring/startsWith checks on “safe-looking” commands.
   - Validate the input shape first, then allow only an exact set of whole commands.

3) **Frame hook behavior as filtering, not security**
   - If hook enforcement can be “too easy to defeat,” document it as removing irrelevant outputs or preventing obvious mistakes—not as a guarantee against compromise.

4) **Prevent secret leakage from workspace-generated configs**
   - Any remote/enterprise settings written into the workspace may include access keys; ensure those generated folders are correctly and recursively gitignored.

Example (command gating via hook with exact matching):
```ts
// In a workflow-controlled PreToolUse hook
// (guardrails example—don’t treat as a sole security boundary)

function approveRunCommands(input: unknown): boolean {
  const typed = input as { commands?: unknown }
  if (!typed || !Array.isArray(typed.commands)) return false

  const safe = new Set([
    'ls',
    'git status',
    'git log --oneline -20',
    // Prefer minimal read-only commands; re-check for repo-specific behaviors
  ])

  return typed.commands.every(
    (cmd) => typeof cmd === 'string' && safe.has(cmd.trim())
  )
}
```

Git ignore reminder (workspace-written enterprise config):
```text
**/.cline/enterprise/
**/.cline/remote-config/
```