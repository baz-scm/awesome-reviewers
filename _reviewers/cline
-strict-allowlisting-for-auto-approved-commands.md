---
title: Strict allowlisting for auto-approved commands
description: When implementing auto-approval or allowlist logic for executing external
  commands (e.g., shell/tool calls), never rely on prefix matching or loose string
  checks like `cmd.startsWith(safe)`—attackers or unexpected arguments can turn a
  "safe" command into a dangerous one (e.g., `git diff --output=<file>` can write
  arbitrary files). Instead, validate the full...
repository: 'cline/cline

  '
label: Security
language: Other
comments_count: 1
repository_stars: 70942
---

When implementing auto-approval or allowlist logic for executing external commands (e.g., shell/tool calls), never rely on prefix matching or loose string checks like `cmd.startsWith(safe)`—attackers or unexpected arguments can turn a "safe" command into a dangerous one (e.g., `git diff --output=<file>` can write arbitrary files). Instead, validate the full input shape first, then match against an exact allowlist of complete command strings (e.g., using a `Set` and comparing trimmed, full commands). Additionally, be aware that even exact "read-only" commands can be unsafe due to environment/tool configuration (e.g., Git's `diff.external` or `core.fsmonitor` can execute arbitrary programs even for `git diff` or `git status`). Document clearly that such auto-approval mechanisms should only be enabled in trusted environments/repositories, and avoid presenting them as universally safe.

Example:
```ts
const input = request.input as { commands?: unknown }

// Exact match against a fixed allowlist; no prefix matching.
if (request.toolName === "run_commands" && Array.isArray(input.commands)) {
  const safeCommands = new Set(["ls", "git status", "git diff", "git log --oneline -20"])
  if (input.commands.every((cmd) => typeof cmd === "string" && safeCommands.has(cmd.trim()))) {
    return { approved: true } // Only safe in repositories you trust; repo config can still run arbitrary programs.
  }
}
```