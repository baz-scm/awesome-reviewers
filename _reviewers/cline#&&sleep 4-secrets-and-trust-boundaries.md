---
title: Secrets and trust boundaries
description: When a feature touches credentials, secrets, or executes code from an
  untrusted source, be explicit and conservative about the trust boundary rather than
  relying on a mechanism that looks secure but isn't.
repository: cline/cline#&&sleep 4
label: Security
language: Other
comments_count: 3
repository_stars: 70980
---

When a feature touches credentials, secrets, or executes code from an untrusted source, be explicit and conservative about the trust boundary rather than relying on a mechanism that looks secure but isn't.

1. Never let code or hooks from an untrusted or attacker-controlled source (e.g. scripts checked out from a pull request) run with access to privileged credentials (tokens, API keys). Scope the job/process permissions tightly (e.g. a minimal `GH_TOKEN` scope), and prefer hooks/config loaded from a trusted, non-checked-out location (global config, base branch) over files that ship inside the untrusted checkout. If untrusted code must run, assume it can read/modify anything in that environment.

2. Don't market or document a control as a "security" boundary if it can be trivially bypassed (e.g. a hook that merely filters file access). Frame such controls accurately (as convenience/filtering features) so users don't mistakenly rely on them for real protection.

3. Any file your tooling writes to a workspace that may contain secrets or sensitive cached config must be excluded from version control with ignore patterns robust enough to catch nested directories, not just the repo root. For example, prefer a recursive pattern:

```text
**/.cline/enterprise/
**/.cline/remote-config/
```

over a root-anchored one, and verify with `git check-ignore` that the pattern matches files in subfolders, since users may run tooling from within a nested directory.

Applying these rules prevents secret leakage into logs, version control, or attacker-controlled execution contexts, and avoids giving users false confidence in weak controls.