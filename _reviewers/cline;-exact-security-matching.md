---
title: Exact security matching
description: When writing security-sensitive allow/deny logic—command allowlists,
  gitignore patterns, path checks—use exact, whole-value matching instead of prefix
  or substring checks, and make sure the pattern covers every context where the check
  applies (nested directories, command flags, external tool configuration). Loose
  matching is easy to bypass:...
repository: cline/cline;
label: Security
language: Other
comments_count: 2
repository_stars: 70964
---

When writing security-sensitive allow/deny logic—command allowlists, gitignore patterns, path checks—use exact, whole-value matching instead of prefix or substring checks, and make sure the pattern covers every context where the check applies (nested directories, command flags, external tool configuration). Loose matching is easy to bypass: `cmd.startsWith("git diff")` also approves `git diff --output=<file>`, which writes a file, and a root-anchored gitignore pattern like `.cline/enterprise/` won't match the same folder nested under a subdirectory, so credentials inside it could still get committed. Prefer matching full tokens against a known-safe set and use recursive patterns for paths:

```ts
// Match whole commands; flags like `git diff --output=<file>` can write files.
const safeCommands = new Set(["ls", "git status", "git diff", "git log --oneline -20"])
if (input.commands.every((cmd) => typeof cmd === "string" && safeCommands.has(cmd.trim()))) {
  return { approved: true }
}
```

```text
# Recursive pattern so nested folders are ignored too; these files can contain
# prompt storage access keys.
**/.cline/enterprise/
**/.cline/remote-config/
```

Also record the underlying threat model in a comment (e.g., "no flag makes this safe in an untrusted repo because `core.fsmonitor`/`diff.external` can still run arbitrary programs") so the rationale for the restriction isn't lost when the code is later modified.</description>
</invoke>
