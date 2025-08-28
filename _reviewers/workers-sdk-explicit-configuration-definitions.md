---
title: Explicit configuration definitions
description: Ensure all configuration dependencies and environment variables are explicitly
  defined rather than relying on implicit behavior or assumptions. This prevents issues
  from version drift, missing definitions, or unclear dependencies.
repository: cloudflare/workers-sdk
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 3379
---

Ensure all configuration dependencies and environment variables are explicitly defined rather than relying on implicit behavior or assumptions. This prevents issues from version drift, missing definitions, or unclear dependencies.

For dependency management, use package manager overrides or explicit version pinning when implicit version ranges could cause compatibility issues:

```yaml
# pnpm override example
overrides:
  vite: "5.4.14"  # Pin to specific version when needed
```

For environment variables, explicitly define all required variables even if they're referenced elsewhere in configuration files:

```yaml
# GitHub Actions example
env:
  CI_OS: ${{ runner.os }}  # Explicitly define, don't just reference
  TEST_PM: ${{ inputs.packageManager }}
```

This approach prevents scenarios where dependencies unexpectedly update ("vitest doesn't pin to vite 5.0 so it can easily get updated to 6 when you're not looking") or where required environment variables are referenced but not properly defined ("we also need to make sure it's defined").