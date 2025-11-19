---
title: scope CI access tokens
description: Configure CI pipelines to use appropriately scoped access tokens based
  on branch protection status. Use read-write tokens only for protected branches (branches
  that don't allow direct push) and read-only tokens for all other branches and environments.
repository: nrwl/nx
label: CI/CD
language: Markdown
comments_count: 6
repository_stars: 27518
---

Configure CI pipelines to use appropriately scoped access tokens based on branch protection status. Use read-write tokens only for protected branches (branches that don't allow direct push) and read-only tokens for all other branches and environments.

Read-write tokens allow full cache access but should be restricted to trusted environments to prevent cache poisoning. Read-only tokens allow reading from the shared primary cache and writing to branch-specific isolated caches, providing cache benefits while maintaining security.

Additionally, ensure CI commands are non-interactive by using appropriate flags like `--yes` to prevent pipelines from hanging on user prompts.

```yaml
# GitHub Actions example
jobs:
  main:
    runs-on: ubuntu-latest
    steps:
      - run: npx nx affected -t build,lint,test
      - run: npx nx release --yes  # Prevent prompts in CI
    env:
      # Use read-write token for protected branches only
      NX_CLOUD_ACCESS_TOKEN: ${{ github.ref == 'refs/heads/main' && secrets.NX_CLOUD_ACCESS_TOKEN_RW || secrets.NX_CLOUD_ACCESS_TOKEN_RO }}
```

This approach prevents unauthorized cache modifications while maintaining the performance benefits of remote caching across all CI runs.