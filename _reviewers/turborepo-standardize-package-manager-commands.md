---
title: Standardize package manager commands
description: Ensure all package manager commands in documentation and CI/CD scripts
  follow the correct syntax for the specific package manager being used, especially
  in monorepo environments. Package manager flags should be positioned correctly according
  to each tool's specifications to prevent pipeline failures.
repository: vercel/turborepo
label: CI/CD
language: Markdown
comments_count: 3
repository_stars: 28115
---

Ensure all package manager commands in documentation and CI/CD scripts follow the correct syntax for the specific package manager being used, especially in monorepo environments. Package manager flags should be positioned correctly according to each tool's specifications to prevent pipeline failures.

When documenting commands for monorepo tools like Turborepo:
1. Clearly distinguish between globally installed and locally installed usage
2. Place package manager flags in their correct position
3. When possible, provide generic guidance that works across different package managers

Example:
```
# Incorrect command (flag placement issue)
pnpm test:interactive -F turborepo-tests-integration

# Correct command
pnpm --filter turborepo-tests-integration test:interactive

# For documentation, consider a more generic approach:
# Without global turbo, use your package manager:
npx turbo build    # for npm
yarn dlx turbo build    # for yarn
pnpm exec turbo build    # for pnpm
```

Proper command syntax is critical for successful CI/CD pipelines, as incorrect commands will cause builds to fail and interrupt deployment workflows.