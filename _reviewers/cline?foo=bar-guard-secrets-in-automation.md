---
title: Guard secrets in automation
description: When an automated workflow runs with privileged credentials (e.g. `GH_TOKEN`,
  API keys) against content from a checked-out branch or repository, treat anything
  sourced from that checkout as untrusted and never let it run with access to those
  secrets. Hooks, plugins, or config files living inside a PR's checkout (`.cline/hooks/`,
  `.clinerules/hooks/`) can be...
repository: cline/cline?foo=bar
label: Security
language: Other
comments_count: 2
repository_stars: 71082
---

When an automated workflow runs with privileged credentials (e.g. `GH_TOKEN`, API keys) against content from a checked-out branch or repository, treat anything sourced from that checkout as untrusted and never let it run with access to those secrets. Hooks, plugins, or config files living inside a PR's checkout (`.cline/hooks/`, `.clinerules/hooks/`) can be modified by the PR author, so don't rely on repo-local enforcement for security-sensitive restrictions — instead check out only the base branch, read changes via a read-only command (e.g. `gh pr diff`), strip known hook/config directories before the sensitive step runs, or enforce restrictions through a global hook/policy outside the checkout rather than one the untrusted content could tamper with.

Likewise, any files your tooling writes that may contain secrets or access tokens (cached configs, credential caches, etc.) must be reliably excluded from version control. Use recursive gitignore patterns rather than root-anchored ones, since tools may be invoked from a subdirectory and a root-anchored pattern will silently miss nested copies:

```text
# Wrong - only matches at repo root
.cline/enterprise/
.cline/remote-config/

# Correct - matches regardless of nesting
**/.cline/enterprise/
**/.cline/remote-config/
```

Verify ignore rules with `git check-ignore` on a nested path, and document why the exclusion exists (e.g. "contains prompt storage access keys") so future contributors don't remove it.</description>
</invoke>
