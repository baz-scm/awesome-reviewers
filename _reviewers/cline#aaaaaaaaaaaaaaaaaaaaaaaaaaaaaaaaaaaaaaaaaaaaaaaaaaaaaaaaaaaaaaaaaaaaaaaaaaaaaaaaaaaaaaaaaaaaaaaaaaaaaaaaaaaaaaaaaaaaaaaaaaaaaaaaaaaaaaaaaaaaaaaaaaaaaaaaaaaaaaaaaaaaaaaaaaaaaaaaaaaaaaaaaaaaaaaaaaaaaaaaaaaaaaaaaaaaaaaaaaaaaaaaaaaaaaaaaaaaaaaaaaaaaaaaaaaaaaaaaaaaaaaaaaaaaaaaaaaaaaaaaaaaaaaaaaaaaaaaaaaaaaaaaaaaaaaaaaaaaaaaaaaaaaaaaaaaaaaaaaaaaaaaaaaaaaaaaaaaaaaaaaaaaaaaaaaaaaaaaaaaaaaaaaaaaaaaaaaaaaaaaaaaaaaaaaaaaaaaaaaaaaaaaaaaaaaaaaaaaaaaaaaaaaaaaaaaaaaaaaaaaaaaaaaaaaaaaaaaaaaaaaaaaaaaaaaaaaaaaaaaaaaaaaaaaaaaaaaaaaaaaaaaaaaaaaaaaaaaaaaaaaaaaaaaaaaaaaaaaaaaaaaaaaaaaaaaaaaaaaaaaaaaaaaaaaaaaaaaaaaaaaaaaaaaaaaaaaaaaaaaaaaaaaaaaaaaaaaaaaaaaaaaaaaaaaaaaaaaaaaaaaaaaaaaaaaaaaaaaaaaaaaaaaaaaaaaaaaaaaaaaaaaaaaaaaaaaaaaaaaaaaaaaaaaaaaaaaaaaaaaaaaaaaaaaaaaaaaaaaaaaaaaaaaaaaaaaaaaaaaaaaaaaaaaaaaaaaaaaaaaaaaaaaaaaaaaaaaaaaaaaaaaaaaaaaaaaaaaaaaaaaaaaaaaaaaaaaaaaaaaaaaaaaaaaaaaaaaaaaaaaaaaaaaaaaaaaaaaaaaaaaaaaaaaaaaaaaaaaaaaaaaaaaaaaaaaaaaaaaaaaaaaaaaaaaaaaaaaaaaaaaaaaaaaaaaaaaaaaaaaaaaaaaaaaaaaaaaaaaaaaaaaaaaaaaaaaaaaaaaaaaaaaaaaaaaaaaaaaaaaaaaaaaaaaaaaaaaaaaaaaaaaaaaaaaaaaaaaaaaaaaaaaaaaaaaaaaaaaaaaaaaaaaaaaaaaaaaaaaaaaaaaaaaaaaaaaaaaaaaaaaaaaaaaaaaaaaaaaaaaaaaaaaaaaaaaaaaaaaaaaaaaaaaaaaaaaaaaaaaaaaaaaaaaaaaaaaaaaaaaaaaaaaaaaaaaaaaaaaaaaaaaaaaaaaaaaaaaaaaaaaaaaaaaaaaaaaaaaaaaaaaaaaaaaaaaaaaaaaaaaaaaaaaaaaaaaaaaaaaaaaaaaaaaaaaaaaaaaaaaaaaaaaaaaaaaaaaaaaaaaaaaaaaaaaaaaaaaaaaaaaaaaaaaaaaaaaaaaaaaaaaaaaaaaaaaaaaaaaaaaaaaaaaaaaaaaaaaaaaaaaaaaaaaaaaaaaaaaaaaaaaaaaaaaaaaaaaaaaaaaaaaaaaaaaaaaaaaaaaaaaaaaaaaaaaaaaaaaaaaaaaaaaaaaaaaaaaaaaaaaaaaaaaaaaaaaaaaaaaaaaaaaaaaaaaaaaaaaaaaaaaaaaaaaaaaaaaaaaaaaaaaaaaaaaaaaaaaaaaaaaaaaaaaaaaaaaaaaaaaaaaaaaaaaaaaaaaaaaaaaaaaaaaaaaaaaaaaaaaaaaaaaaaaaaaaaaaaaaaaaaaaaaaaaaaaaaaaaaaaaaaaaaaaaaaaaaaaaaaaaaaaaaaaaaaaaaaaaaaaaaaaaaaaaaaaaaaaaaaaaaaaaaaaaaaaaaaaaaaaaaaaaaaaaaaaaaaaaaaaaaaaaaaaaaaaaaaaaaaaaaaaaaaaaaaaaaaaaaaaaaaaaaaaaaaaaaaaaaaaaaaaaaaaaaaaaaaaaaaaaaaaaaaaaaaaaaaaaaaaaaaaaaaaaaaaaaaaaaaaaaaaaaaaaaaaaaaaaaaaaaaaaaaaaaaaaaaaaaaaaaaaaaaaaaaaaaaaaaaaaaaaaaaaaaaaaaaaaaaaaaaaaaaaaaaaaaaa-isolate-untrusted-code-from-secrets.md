---
title: Isolate untrusted code from secrets
description: When building automation that auto-approves or executes commands/hooks/plugins,
  never trust input from an untrusted source (model output, a checked-out branch,
  or a nested folder) without strict validation.
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Security
language: Other
comments_count: 3
repository_stars: 70976
---

When building automation that auto-approves or executes commands/hooks/plugins, never trust input from an untrusted source (model output, a checked-out branch, or a nested folder) without strict validation.

- For auto-approval allowlists, match whole commands exactly against a fixed set, never by prefix. Prefix matching can be bypassed (e.g. `git diff` can be hijacked via `diff.external` or `core.fsmonitor` in a repo's config), so no combination of flags makes a command inherently "safe" in a repository you don't control/trust.
  ```ts
  // Bad: prefix match is bypassable via repo-local git config
  if (safeCommands.some((safe) => cmd.startsWith(safe))) { ... }

  // Good: exact match against a fixed allowlist, only in trusted repos
  const safeCommands = new Set(["ls", "git status", "git diff", "git log --oneline -20"])
  if (input.commands.every((cmd) => safeCommands.has(cmd.trim()))) { ... }
  ```
- In CI or any pipeline where privileged credentials (tokens, secrets) are in the environment, do not let code from an untrusted checkout (e.g. a pull request branch) execute with that environment. Hooks and plugins loaded from a repository's own config folders run with full access to `process.env`, so a malicious PR can exfiltrate secrets. Prefer checking out the base branch and fetching the diff via an API call, or strip/delete any repo-local hook/plugin folders before the privileged step runs. Only rely on a global, out-of-repo hook as a secondary allow/deny gate — it is not a substitute for not exposing secrets to untrusted code in the first place.
- Never let sensitive cached data (API keys, tokens, synced settings) land in version control. Add them to `.gitignore`, and use recursive patterns (`**/.cline/enterprise/`) rather than root-anchored ones, since root-anchored patterns silently fail to match the same folder created in a nested subdirectory. Verify ignore rules with `git check-ignore` against a nested path, not just the repo root.

Treat every boundary where external input (model output, a PR's files, a nested directory) meets a privileged action (shell execution, secret access, git tracking) as a security boundary, and default to the most restrictive, explicitly-verified rule rather than a convenient heuristic.</description>
</invoke>
