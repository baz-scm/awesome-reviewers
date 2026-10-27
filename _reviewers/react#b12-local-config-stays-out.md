---
title: Local config stays out
description: 'Keep environment- and user-specific configuration out of version control,
  and make any required environment-dependent setup steps explicit.


  - Add user/local files (e.g., `settings.local.json` or `*.local.json`) to `.gitignore`.'
repository: facebook/react#b12
label: Configurations
language: Json
comments_count: 2
repository_stars: 251896
---

Keep environment- and user-specific configuration out of version control, and make any required environment-dependent setup steps explicit.

- Add user/local files (e.g., `settings.local.json` or `*.local.json`) to `.gitignore`.
- Commit a shared baseline config (e.g., `settings.json`) that teams can use consistently.
- If dependency changes are tied to a specific OS/tooling quirk (or require non-default install behavior, such as ignoring optional deps), document the exact command/flag in the repo (e.g., in the PR description and/or a README).

Example:
```gitignore
# user-specific settings
compiler/.claude/settings.local.json
# alternatively, a pattern
# *.local.json
```

```bash
# when a change requires it (document this in-repo)
yarn install --ignore-optional
```