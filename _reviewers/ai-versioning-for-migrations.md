---
title: Versioning for migrations
description: Use appropriate version bumps to signal migration requirements and maintain
  clear upgrade paths. Flag breaking changes with major version bumps to help with
  release notes and upgrade guides. External contributors should use patch bumps only,
  while minor and major version changes are reserved for the core team.
repository: vercel/ai
label: Migrations
language: Markdown
comments_count: 2
repository_stars: 15590
---

Use appropriate version bumps to signal migration requirements and maintain clear upgrade paths. Flag breaking changes with major version bumps to help with release notes and upgrade guides. External contributors should use patch bumps only, while minor and major version changes are reserved for the core team.

Example:
```
# For breaking changes (core team only)
pnpm changeset
# Select 'major' for the bump type when removing APIs or making breaking changes

# For external contributors
pnpm changeset
# Select 'patch' for all contribution changes
```

This versioning strategy ensures users have clear signals about migration requirements and proper documentation is maintained for version transitions.