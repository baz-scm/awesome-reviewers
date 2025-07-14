---
title: Maintain portable config values
description: 'Always use portable, environment-agnostic values in configuration files.
  Avoid hardcoded absolute paths, system-specific values, or mismatched feature flags.
  Instead:'
repository: oven-sh/bun
label: Configurations
language: Other
comments_count: 3
repository_stars: 79093
---

Always use portable, environment-agnostic values in configuration files. Avoid hardcoded absolute paths, system-specific values, or mismatched feature flags. Instead:

1. Use relative paths and environment variables
2. Ensure error messages accurately reflect configuration conditions
3. Use correct and specific feature flags for analytics and tracking

Example - Instead of:
```cmake
-Wl,-non_global_symbols_no_strip_list,/Users/username/project/src/symbols.txt
bun.Analytics.Features.lockfile_migration_from_package_lock += 1  # for pnpm migration
```

Use:
```cmake
-Wl,-non_global_symbols_no_strip_list,${CMAKE_SOURCE_DIR}/src/symbols.txt
bun.Analytics.Features.lockfile_migration_from_pnpm_lock += 1  # specific to migration type
```

This ensures configurations work consistently across different environments and accurately reflect system behavior.