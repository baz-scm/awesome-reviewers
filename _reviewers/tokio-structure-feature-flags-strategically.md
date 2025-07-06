---
title: Structure feature flags strategically
description: Design feature flags to minimize dependency bloat while maximizing flexibility
  for users. Each optional dependency should be tied to a specific feature flag, allowing
  users to enable only the functionality they need.
repository: tokio-rs/tokio
label: Configurations
language: Toml
comments_count: 5
repository_stars: 28989
---

Design feature flags to minimize dependency bloat while maximizing flexibility for users. Each optional dependency should be tied to a specific feature flag, allowing users to enable only the functionality they need.

Key practices:
1. Express dependencies between features explicitly in Cargo.toml
2. Create granular feature flags for optional dependencies
3. Use conditional compilation for platform or feature-specific code
4. Consider feature organization when adding new functionality

For example, instead of requiring a dependency for all users:

```toml
# Avoid this approach - forces dependency on all users
rt = ["tokio/rt", "tokio/sync", "futures-util", "hashbrown"]
```

Use a more targeted approach:

```toml
# Better approach - separate optional functionality
rt = ["tokio/rt", "tokio/sync", "futures-util"]
join-map = ["rt", "hashbrown"]
```

For platform-specific features, use appropriate conditional compilation:

```toml
# For platform-specific features
[target.'cfg(all(target_os = "linux", feature = "rt"))'.dependencies]
# Linux-specific dependencies here
```

When organizing features, aim for a balance between granularity and usability, with a "full" feature that enables everything for convenience.