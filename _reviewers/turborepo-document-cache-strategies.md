---
title: Document cache strategies
description: 'Always provide clear documentation and implementation for caching strategies,
  including key generation, invalidation policies, and default behaviors. When implementing
  caching:'
repository: vercel/turborepo
label: Caching
language: Other
comments_count: 3
repository_stars: 28115
---

Always provide clear documentation and implementation for caching strategies, including key generation, invalidation policies, and default behaviors. When implementing caching:

1. Choose appropriate cache keys that balance specificity and reusability:
   - For CI environments, consider using commit SHA with restore-keys fallback:
   ```yaml
   - uses: actions/cache@v4
     with:
       path: .turbo
       key: ${{ runner.os }}-turbo-${{ github.sha }}
       restore-keys: |
         ${{ runner.os }}-turbo-
   ```

2. Document cache configuration options explicitly:
   - Explain what happens when cache configuration is missing
   - Specify available cache sources and their permissions (e.g., local vs. remote)
   - Describe the behavior of cache invalidation

3. Make cache behavior predictable and configurable:
   - Allow users to control cache sources (e.g., `--cache=local:rw,remote:r`)
   - Provide clear indicators when caching is enabled/disabled
   - Document which artifacts will be cached by default

Proper cache strategy documentation prevents unexpected behavior, improves performance, and gives users control over how and where their data is cached.