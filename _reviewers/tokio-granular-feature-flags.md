---
title: Granular feature flags
description: Feature flags should be designed with granularity to ensure dependencies
  are only required when absolutely necessary. When adding functionality that requires
  additional dependencies, create separate features rather than adding those dependencies
  to existing features.
repository: tokio-rs/tokio
label: Configurations
language: Toml
comments_count: 4
repository_stars: 28981
---

Feature flags should be designed with granularity to ensure dependencies are only required when absolutely necessary. When adding functionality that requires additional dependencies, create separate features rather than adding those dependencies to existing features.

Key principles:
1. Make dependencies optional whenever possible
2. Create dedicated features for functionality requiring specific dependencies
3. Consider feature dependencies carefully to avoid unnecessary inclusions
4. Disable default features of dependencies when only specific functionality is needed

Example:
```toml
# GOOD: Granular feature with minimal dependencies
[features]
rt = ["tokio/rt", "tokio/sync", "futures-util"]
join-map = ["rt", "hashbrown"]  # Separate feature for hashbrown dependency

# BAD: Requiring hashbrown for all rt users
[features]
rt = ["tokio/rt", "tokio/sync", "futures-util", "hashbrown"]
```

This approach keeps the dependency tree minimal for users who don't need specific functionality, improving compile times and reducing potential version conflicts. When considering target-specific configurations, ensure dependencies are properly scoped to the relevant target and features (e.g., `#[cfg(all(target_os = "linux", feature = "rt"))]`).