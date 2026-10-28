---
title: Untrusted input and secret isolation
description: Treat any code, config, or hook that can be influenced by untrusted sources
  (a checked-out pull request, a user-writable workspace subfolder, model-controlled
  logic) as untrusted, and never let it run with access to privileged credentials
  or silently persist sensitive data where it can be committed.
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Security
language: Other
comments_count: 3
repository_stars: 70984
---

Treat any code, config, or hook that can be influenced by untrusted sources (a checked-out pull request, a user-writable workspace subfolder, model-controlled logic) as untrusted, and never let it run with access to privileged credentials or silently persist sensitive data where it can be committed.

Apply this in practice:
- In CI/CD pipelines, don't assume repo-local hooks/plugins (e.g. `.cline/hooks/`, `.clinerules/hooks/`) are safe to execute with the job's environment — a pull request can modify them to exfiltrate secrets like `GH_TOKEN`. Either check out only the base branch and read PR changes via a diff command, strip those directories before the privileged step, or enforce restrictions via a global hook/config that lives outside the untrusted checkout, not one shipped in the repository.
- Any mechanism that depends on the model (or other non-enforced logic) choosing to comply should not be documented or relied on as a security boundary — it's trivially bypassable. Frame such features honestly (e.g. as convenience filtering) and provide a real, enforced control (deny lists, permission blocks, sandboxing) for anything security-sensitive.
- When sensitive data (tokens, keys, cached credentials) is written to the workspace, ensure it's excluded from version control with patterns robust to any directory nesting, since the sensitive folder may not always be at the workspace root. Prefer recursive glob patterns over root-anchored ones, e.g.:

```text
**/.cline/enterprise/
**/.cline/remote-config/
```

Verify exclusion patterns actually match in all expected scenarios (e.g. with `git check-ignore`) before relying on them.</description>
</invoke>
