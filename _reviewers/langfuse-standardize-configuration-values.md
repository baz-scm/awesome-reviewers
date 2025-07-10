---
title: Standardize configuration values
description: 'Always standardize configuration values to ensure consistency, reproducibility,
  and maintainability:


  1. **Pin specific versions** instead of using floating tags for dependencies to
  ensure consistent behavior across environments.'
repository: langfuse/langfuse
label: Configurations
language: Yaml
comments_count: 3
repository_stars: 13574
---

Always standardize configuration values to ensure consistency, reproducibility, and maintainability:

1. **Pin specific versions** instead of using floating tags for dependencies to ensure consistent behavior across environments.
   ```diff
   - image: redis:6.0
   + image: redis:6.0.20
   ```

2. **Centralize repeated values** as environment variables or constants to avoid duplication and simplify updates.
   ```diff
   - curl -L https://github.com/golang-migrate/migrate/releases/download/v4.18.3/migrate.linux-amd64.tar.gz | tar xvz
   + MIGRATE_VERSION="v4.18.3"
   + curl -L https://github.com/golang-migrate/migrate/releases/download/$MIGRATE_VERSION/migrate.linux-amd64.tar.gz | tar xvz
   ```

3. **Use official defaults** when configuring services, then provide clear documentation for any custom values and ensure they can be overridden when needed.
   ```yaml
   # Use environment variables with descriptive comments
   CLICKHOUSE_MAX_MEMORY_USAGE: "${CLICKHOUSE_MEM:-800000000}"  # Default ~800MB, override with CLICKHOUSE_MEM
   ```

This approach reduces maintenance burden, makes configuration changes safer and more deliberate, and provides better visibility into how systems are configured.