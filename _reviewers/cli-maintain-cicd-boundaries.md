---
title: maintain CI/CD boundaries
description: Ensure clear separation between different CI/CD concerns and maintain
  accurate documentation of automated processes. Release artifacts like release notes
  should not be committed to main development branches, and testing workflows should
  be clearly documented with accurate branch-specific behaviors.
repository: snyk/cli
label: CI/CD
language: Markdown
comments_count: 2
repository_stars: 5178
---

Ensure clear separation between different CI/CD concerns and maintain accurate documentation of automated processes. Release artifacts like release notes should not be committed to main development branches, and testing workflows should be clearly documented with accurate branch-specific behaviors.

For release management, keep release notes and similar artifacts in dedicated release branches or automated release processes rather than cluttering the main development branch. For testing documentation, ensure accuracy in describing when and how different test suites execute, including branch-specific triggers and scheduling.

Example of proper smoke test documentation:
```markdown
### Smoke Tests

Smoke tests typically don't run on branches unless the branch is specifically prefixed with `smoke/`. They usually run on an hourly basis against the latest published version of the CLI.
```

This maintains clear boundaries between development work, release processes, and testing workflows, making the CI/CD pipeline more predictable and maintainable.