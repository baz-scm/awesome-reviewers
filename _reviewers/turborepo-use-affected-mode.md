---
title: Use affected mode
description: Optimize CI pipelines by running tasks only on packages affected by code
  changes. Use the `--affected` flag in Turborepo commands to automatically filter
  tasks to packages with changes, significantly reducing CI execution time in large
  monorepos.
repository: vercel/turborepo
label: CI/CD
language: Other
comments_count: 3
repository_stars: 28115
---

Optimize CI pipelines by running tasks only on packages affected by code changes. Use the `--affected` flag in Turborepo commands to automatically filter tasks to packages with changes, significantly reducing CI execution time in large monorepos.

```bash
# Run build only on affected packages
turbo run build --affected

# Specify custom base branch for comparison
TURBO_SCM_BASE=development turbo run test --affected
```

By default, affected mode compares changes between `main` and `HEAD`. Override these defaults with environment variables `TURBO_SCM_BASE` and `TURBO_SCM_HEAD` when needed, such as when working with feature branches or alternative main branches.

Ensure your checkout has sufficient history depth; shallow clones may cause all packages to be considered changed. This approach ensures CI resources are used efficiently by focusing only on what changed, preventing unnecessary builds and tests while maintaining comprehensive validation.