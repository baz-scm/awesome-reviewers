---
title: Enforce real trust boundaries
description: Do not present or rely on a control as a security boundary if it can
  be bypassed or altered by the very input it's meant to constrain. Hooks, plugins,
  allowlists, and auto-approval rules that live inside a model's context, a repository
  checkout, or a pull request are not safe guards against that same model or that
  same repository/PR content — a hostile...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Security
language: Other
comments_count: 4
repository_stars: 70973
---

Do not present or rely on a control as a security boundary if it can be bypassed or altered by the very input it's meant to constrain. Hooks, plugins, allowlists, and auto-approval rules that live inside a model's context, a repository checkout, or a pull request are not safe guards against that same model or that same repository/PR content — a hostile actor can simply edit or disable them. Document these as convenience/filtering features, not security controls, and enforce real restrictions from a location the untrusted input cannot reach (e.g., CI job `permissions`, checking out the base branch instead of the PR, deleting untrusted hook/plugin folders before running privileged steps, or a global hook stored outside the workspace).

When building allowlists for auto-approval of "safe" commands, avoid prefix/substring matching and remember that external tool configuration (e.g., git's `diff.external`, `core.fsmonitor`) can make even nominally read-only commands execute arbitrary programs. Match whole commands against a fixed, trusted set, and call out in comments/docs that such approvals are only safe in repositories you already trust — there is no flag or wrapper that makes an untrusted repo safe to auto-approve commands in.

Finally, when a tool writes cached credentials or other sensitive config to disk inside a workspace, exclude it from version control with ignore patterns that work regardless of where in the repo the command runs (prefer recursive patterns like `**/.cline/enterprise/` over root-anchored ones like `.cline/enterprise/`, and verify with `git check-ignore` against a nested path).

Example:
```text
# Recursive — matches at any depth
**/.cline/enterprise/
**/.cline/remote-config/

# Root-anchored — misses nested checkouts, avoid
.cline/enterprise/
```
```ts
// Match whole, trusted commands only; do not rely on prefix checks
const safeCommands = new Set(["ls", "git status", "git log --oneline -20"])
if (input.commands.every((cmd) => typeof cmd === "string" && safeCommands.has(cmd.trim()))) {
  // Safe only in repositories you already trust
  return { approved: true }
}
```