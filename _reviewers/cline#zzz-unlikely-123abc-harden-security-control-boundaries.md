---
title: Harden security control boundaries
description: 'When documenting or implementing any mechanism intended to restrict,
  approve, or isolate behavior (allowlists, hooks, ignore patterns, permission checks),
  verify it actually closes every bypass path and never label it as a security boundary
  unless it does. Specifically:'
repository: cline/cline#zzz-unlikely-123abc
label: Security
language: Other
comments_count: 4
repository_stars: 71035
---

When documenting or implementing any mechanism intended to restrict, approve, or isolate behavior (allowlists, hooks, ignore patterns, permission checks), verify it actually closes every bypass path and never label it as a security boundary unless it does. Specifically:

1. Don't mis-frame weak mechanisms as security. If a control (e.g. a `.clineignore` hook) can be trivially defeated by the untrusted party it's meant to restrict, either harden it or re-describe its purpose honestly (e.g. "filtering irrelevant files") rather than presenting it as a security guarantee.

2. Allowlists must account for indirect execution paths, not just the literal command string. For example, approving `git diff` as "safe" ignores that `diff.external` or `core.fsmonitor` config can make it run arbitrary programs. Match whole commands conservatively, and document that such lists are only safe in repositories/environments you already trust — no set of flags makes an untrusted repo safe.

3. Never let untrusted, attacker-influenced input execute with trusted credentials. If a CI job checks out a pull request, don't rely on hooks/plugins from that checkout (`.cline/hooks/`, `.cline/plugins/`) to enforce restrictions — the PR can modify them, and they'll still run with the job's secrets (e.g. `GH_TOKEN`). Prefer global, out-of-repo enforcement, or avoid checking out untrusted code when only a diff is needed (e.g. `gh pr diff`).

4. When excluding sensitive cached data from version control, use recursive glob patterns (`**/.cline/enterprise/`) instead of root-anchored ones (`.cline/enterprise/`), since root-anchored patterns miss the same folder created in a subdirectory. Validate exclusions with `git check-ignore` against nested paths.

In short: treat every security-relevant control as potentially bypassable until you've enumerated the bypass paths, keep trusted and untrusted inputs/credentials strictly separated, and verify defensive patterns cover all real-world locations, not just the common case.