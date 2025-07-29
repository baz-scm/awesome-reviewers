---
title: Document configuration rationale
description: When adding or modifying configuration files, always include clear comments
  or documentation explaining the reasoning behind non-obvious choices, especially
  when suppressing warnings, excluding files, or making decisions that deviate from
  defaults.
repository: remix-run/react-router
label: Configurations
language: Other
comments_count: 3
repository_stars: 55270
---

When adding or modifying configuration files, always include clear comments or documentation explaining the reasoning behind non-obvious choices, especially when suppressing warnings, excluding files, or making decisions that deviate from defaults.

Configuration decisions often involve trade-offs or address specific operational issues that may not be immediately apparent to other developers. Documenting the rationale helps prevent future confusion and accidental reversions.

Examples of good documentation:
```
# .npmrc
# Suppress workspace cycle warnings for dev dependencies in test code
ignore-workspace-cycles=true

# Keep pre/post script behavior during migration to minimize changes
enable-pre-post-scripts=true
```

```
# .eslintignore
# Exclude lock file to prevent CI formatting loops between pnpm and Prettier
pnpm-lock.yaml
```

This practice is particularly important for suppressions, exclusions, and migration-related configurations where the reasoning may not be obvious from the configuration itself.