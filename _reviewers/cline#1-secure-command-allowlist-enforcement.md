---
title: Secure command allowlist enforcement
description: When building allow/deny lists or hooks that gate what an agent or CI
  job can execute, design them as if the input is adversarial — don't treat naive
  string/prefix matching or user-controllable scripts as a real security boundary.
repository: cline/cline#1
label: Security
language: Other
comments_count: 3
repository_stars: 71024
---

When building allow/deny lists or hooks that gate what an agent or CI job can execute, design them as if the input is adversarial — don't treat naive string/prefix matching or user-controllable scripts as a real security boundary.

- Validate the full shape and semantics of a command/tool call, not just its literal prefix. Commands that look read-only can still have side effects through configuration (e.g. `git diff` can run an external program via `diff.external`, or trigger `core.fsmonitor`). Prefer exact matches against a small, well-understood set, and document that "safe" commands are only safe in repositories/environments you trust:

```ts
// Only exact matches; a `startsWith` check lets flags like
// `git diff --output=<file>` sneak through.
const safeCommands = new Set(["ls", "git status", "git diff", "git log --oneline -20"])
if (input.commands.every((cmd) => typeof cmd === "string" && safeCommands.has(cmd.trim()))) {
  return { approved: true } // only safe in repos you trust
}
```

- Never let the untrusted input control the enforcement mechanism itself. For example, in a CI job that checks out a pull request, don't rely on hooks/plugins living in that same checkout (`.cline/hooks/`, `.cline/plugins/`) — the PR can modify them before they run, and they inherit the job's full environment (including secrets like `GH_TOKEN`). Enforce restrictions from outside the untrusted scope instead: check out only the base branch and read PR changes via a read-only API, delete repo-local hook/plugin directories before running, or use a global hook (e.g. `~/.cline/hooks/`) that the untrusted content cannot alter.
- Scope permissions at the source whenever possible (e.g. limit the token/credentials granted to the job) rather than depending solely on an application-level allowlist to prevent misuse.
- Don't document or present these filtering mechanisms as guaranteed security controls when they can be trivially bypassed. If a mechanism is only meant to filter noise (e.g. keep an agent from reading irrelevant files like build output), state that explicitly instead of implying it blocks malicious access.