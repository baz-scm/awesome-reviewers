---
title: Pin testing dependency versions
description: Always specify explicit versions for testing frameworks and tools to
  ensure reproducible test environments across different deployment contexts. Avoid
  installing testing dependencies with implicit "latest" versions, which can lead
  to inconsistent test behavior and difficult-to-debug failures.
repository: browser-use/browser-use
label: Testing
language: Dockerfile
comments_count: 3
repository_stars: 69139
---

Always specify explicit versions for testing frameworks and tools to ensure reproducible test environments across different deployment contexts. Avoid installing testing dependencies with implicit "latest" versions, which can lead to inconsistent test behavior and difficult-to-debug failures.

Use environment variables or extract versions from dependency manifests rather than hard-coding versions directly in installation commands:

```dockerfile
# Option 1: Using environment variables
RUN pip install playwright==$PLAYWRIGHT_VERSION

# Option 2: Extract from dependency manifest
RUN PLAYWRIGHT_VERSION=$(grep -oP 'playwright>=\K[0-9.]+' pyproject.toml) \
    && pip install playwright==$PLAYWRIGHT_VERSION
```

This practice is especially critical in containerized environments where test dependencies need to remain consistent across development, CI/CD, and production testing scenarios. Version pinning prevents unexpected test failures caused by breaking changes in testing framework updates and ensures that test results are reproducible across different environments and time periods.