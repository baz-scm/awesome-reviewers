---
title: Isolate secrets from untrusted content
description: When a CI job or workspace handles a checkout of untrusted content (e.g.,
  a pull request branch) alongside privileged credentials (tokens, API keys), never
  let that untrusted content execute with access to those secrets. Hooks, plugins,
  or config files sourced from the checkout (such as `.cline/hooks/`, `.clinerules/hooks/`,
  `.cline/plugins/`) run with the...
repository: cline/cline?ref=main
label: Security
language: Other
comments_count: 2
repository_stars: 70980
---

When a CI job or workspace handles a checkout of untrusted content (e.g., a pull request branch) alongside privileged credentials (tokens, API keys), never let that untrusted content execute with access to those secrets. Hooks, plugins, or config files sourced from the checkout (such as `.cline/hooks/`, `.clinerules/hooks/`, `.cline/plugins/`) run with the full process environment, including secrets like `GH_TOKEN`, so an attacker can modify them via the PR itself to exfiltrate credentials or run arbitrary commands. Prefer architectures that avoid checking out untrusted refs into a privileged environment (e.g., check out the base branch and fetch diffs via API) or explicitly strip/delete untrusted hook and plugin directories before any privileged step runs. Only rely on security-enforcing hooks when they come from a trusted, non-checkout location (e.g., global hook directories), never from the repository under review.

Similarly, any local files or caches that may contain secrets (such as cached remote-configuration data with prompt storage access keys) must be excluded from version control with gitignore patterns robust to nested workspaces. Use recursive glob patterns rather than root-anchored ones, since a user may open a subdirectory of the repository as their working directory:

```text
# Wrong: only matches at repo root
.cline/enterprise/
.cline/remote-config/

# Correct: matches at any depth
**/.cline/enterprise/
**/.cline/remote-config/
```

Verify exclusion patterns with `git check-ignore` against nested paths to confirm secrets can never be accidentally committed.</description>
</invoke>
