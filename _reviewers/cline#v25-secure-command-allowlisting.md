---
title: Secure Command Allowlisting
description: 'When a system auto-approves or autonomously executes shell/tool commands,
  treat command execution as a high-risk authorization decision:


  - Validate tool input shape before evaluating safety (e.g., ensure `commands` is
  an array of strings).'
repository: cline/cline#v25
label: Security
language: Other
comments_count: 2
repository_stars: 70891
---

When a system auto-approves or autonomously executes shell/tool commands, treat command execution as a high-risk authorization decision:

- Validate tool input shape before evaluating safety (e.g., ensure `commands` is an array of strings).
- Use strict allowlists with exact matches, not prefix/substring checks. Flags can change behavior; “whole command” matching is safer.
- Don’t assume “read-only” tools (notably Git) are safe: repository configuration and flags can cause execution of external programs. Only allow such commands in repositories you explicitly trust.
- Enforce controls from a trusted location. In CI/autonomous runs, never rely on hooks/plugins from the checked-out PR/repo—those files are untrusted and run with the job’s environment (including tokens). Prefer global/out-of-repo enforcement (e.g., a global `PreToolUse` hook) or remove/override `.cline` artifacts before the step.

Example (strict approval of a fixed command set):
```ts
requestToolApproval: async (request) => {
  // Validate input shape
  const input = request.input as { commands?: unknown; files?: unknown }

  const safeCommands = new Set([
    'ls',
    'git status',
    // Avoid broad Git diffs; only allow exact, vetted commands
  ])

  if (request.toolName === 'run_commands' && Array.isArray(input.commands)) {
    const commands = input.commands
    const allAllowed = commands.every(
      (cmd) => typeof cmd === 'string' && safeCommands.has(cmd.trim())
    )

    // Only approve Git commands when the repository is trusted
    if (allAllowed /* && repoIsTrusted */) {
      return { approved: true }
    }
  }

  return { approved: false }
}
```

Team standard: any change to auto-approval/tool-execution logic must include (1) strict input validation, (2) exact-match allowlisting, (3) explicit trust-boundaries for repository-dependent commands, and (4) enforcement that cannot be altered by the PR checkout.