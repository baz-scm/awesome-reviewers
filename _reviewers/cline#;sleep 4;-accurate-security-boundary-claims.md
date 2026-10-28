---
title: Accurate security boundary claims
description: When documenting or implementing any restriction meant to protect users
  (hooks, auto-approve allowlists, permission checks, ignore patterns), verify the
  mechanism actually enforces the boundary it claims to, and never label something
  as a security control if it can be trivially bypassed.
repository: cline/cline#;sleep 4;
label: Security
language: Other
comments_count: 4
repository_stars: 70976
---

When documenting or implementing any restriction meant to protect users (hooks, auto-approve allowlists, permission checks, ignore patterns), verify the mechanism actually enforces the boundary it claims to, and never label something as a security control if it can be trivially bypassed.

- Don't market non-security filters as security: if a hook or check only filters irrelevant content (e.g. build output), describe it that way instead of implying it blocks malicious behavior, since it is easy to defeat.
- Use exact allowlisting, not prefix/substring checks, for commands or inputs that gate privileged actions. `cmd.startsWith(safe)` can match unsafe variants (e.g. `git diff --output=file`); match the whole command string against a fixed set instead.
- Treat configuration and tooling in untrusted repositories as attacker-controlled. Repo-level git config (`diff.external`, `core.fsmonitor`) can execute arbitrary programs even behind "safe" commands like `git diff`/`git status`; only auto-approve such commands in repositories you trust, and document that no flag makes them universally safe.
- When running automation against untrusted input (e.g. a CI job that checks out a pull request), assume any hooks/plugins/config in that checkout are attacker-controlled and will run with the job's full environment (including secrets like `GH_TOKEN`). Don't rely on in-repo enforcement files for restricting such jobs; instead check out the base branch and read the diff separately, strip the config directories before executing, or enforce restrictions via hooks stored outside the checkout (e.g. global `~/.cline/hooks/`).
- When excluding sensitive paths (e.g. `.gitignore` for cached credentials or config), use recursive patterns (`**/.cline/enterprise/`) rather than root-anchored ones, since nested workspace folders can otherwise cause secrets to be committed. Verify ignore patterns with `git check-ignore` against nested paths.

Example of a safer allowlist check:
```ts
const safeCommands = new Set(["ls", "git status", "git log --oneline -20"]) // no git diff: diff.external/core.fsmonitor can run arbitrary programs
if (input.commands.every((cmd) => typeof cmd === "string" && safeCommands.has(cmd.trim()))) {
  return { approved: true }
}
```