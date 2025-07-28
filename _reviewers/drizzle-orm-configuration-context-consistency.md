---
title: Configuration context consistency
description: Ensure configuration names, values, and settings accurately reflect their
  intended context and usage. Configuration mismatches can lead to runtime errors,
  incorrect behavior, and maintenance issues.
repository: drizzle-team/drizzle-orm
label: Configurations
language: TypeScript
comments_count: 4
repository_stars: 29461
---

Ensure configuration names, values, and settings accurately reflect their intended context and usage. Configuration mismatches can lead to runtime errors, incorrect behavior, and maintenance issues.

Key practices:
- Match configuration names to their actual context (e.g., use 'mysql' folder names in MySQL introspection functions, not 'postgresql')
- Use generic, extensible configuration structures when the setting applies to multiple contexts (e.g., `set: { configs: [...], role: ... }` instead of `rlsConfig` for PostgreSQL transaction settings)
- Verify runtime configurations work across target environments and Node.js versions
- Configure build tools with strict settings to catch configuration inconsistencies early

Example of good configuration naming:
```ts
// Instead of context-specific naming
interface PgTransactionConfig {
  rlsConfig?: { ... };
}

// Use generic, extensible naming
interface PgTransactionConfig {
  set?: {
    configs?: {
      name: string;
      value: string;
      isLocal?: boolean;
    }[];
    role?: AnyPgRole;
  };
}
```

This approach prevents configuration drift and makes code more maintainable when contexts change or expand.