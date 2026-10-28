---
title: Isolate untrusted execution and secrets
description: Treat any code, config, or hook that can be influenced by an untrusted
  source (e.g. files checked out from a pull request, user-supplied scripts) as hostile,
  and never let it run with privileged credentials. In CI, don't rely on repo-local
  hooks/plugins (`.cline/hooks/`, `.cline/plugins/`) to enforce restrictions when
  the job checks out a PR, since the PR...
repository: "cline/cline\t"
label: Security
language: Other
comments_count: 3
repository_stars: 70947
---

Treat any code, config, or hook that can be influenced by an untrusted source (e.g. files checked out from a pull request, user-supplied scripts) as hostile, and never let it run with privileged credentials. In CI, don't rely on repo-local hooks/plugins (`.cline/hooks/`, `.cline/plugins/`) to enforce restrictions when the job checks out a PR, since the PR itself can modify those files; instead check out the base branch, strip those folders before the privileged step, or enforce restrictions via a hook stored outside the repo (e.g. `~/.cline/hooks/`) that isn't subject to PR modification. Also avoid documenting or implementing mechanisms as "security" controls when they're trivially bypassable (e.g. a script-based filter that only discourages, rather than blocks, access) — frame such features by their real purpose (convenience/filtering) instead of implying a security guarantee that doesn't hold. Finally, when a tool writes cached settings, keys, or tokens into the workspace, ensure they're excluded from version control with gitignore patterns that match regardless of nesting (use recursive patterns like `**/.cline/enterprise/` rather than root-anchored `.cline/enterprise/`), since a root-anchored pattern won't match the folder when someone opens a subdirectory of the repo, risking an accidental commit of secrets. For example:
```text
# Wrong: only matches at repo root
.cline/enterprise/

# Right: matches at any depth
**/.cline/enterprise/
**/.cline/remote-config/
```
