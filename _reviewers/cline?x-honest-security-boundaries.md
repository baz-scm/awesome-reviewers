---
title: Honest security boundaries
description: When building any mechanism meant to restrict, filter, or gate actions
  on behalf of a user (approval allowlists, hooks, CI permission settings, cached
  config on disk), explicitly define the trust boundary and never claim a guarantee
  the mechanism cannot actually enforce.
repository: cline/cline?x
label: Security
language: Other
comments_count: 4
repository_stars: 70983
---

When building any mechanism meant to restrict, filter, or gate actions on behalf of a user (approval allowlists, hooks, CI permission settings, cached config on disk), explicitly define the trust boundary and never claim a guarantee the mechanism cannot actually enforce.

- Don't market a bypassable control as "security." A script-based hook that a model can simply route around should be documented for its real purpose (e.g., filtering out irrelevant files) rather than presented as a protection the user can rely on.
- When whitelisting "safe" commands for auto-approval, verify there are no hidden side effects before trusting a flag or subcommand. For example, `git diff` can execute arbitrary programs via `diff.external`, and `core.fsmonitor` can run a hook from `git status`/`git diff` as well — no combination of flags makes these safe in a repository you don't already trust. State that limitation explicitly rather than implying the allowlist is universally safe.
- In pipelines that execute untrusted content (e.g., checking out a pull request), never rely on config shipped inside that untrusted checkout (local hooks, plugins, permission files) to enforce restrictions — the untrusted content can modify or disable that very config. Enforce restrictions from outside the untrusted scope instead: use global/host-level hooks, read untrusted diffs without executing them (`gh pr diff`), check out a trusted base ref, or delete local hook/plugin directories before running any agentic step.
- Any sensitive artifact Cline writes to the working directory (access keys, cached org settings, etc.) must be excluded from version control with gitignore patterns that match regardless of nesting (`**/.cline/remote-config/`, not `/.cline/remote-config/`), since a user could be working from any subfolder. Verify the pattern with `git check-ignore` against a nested path, and document why the exclusion is required.</description>
</invoke>
