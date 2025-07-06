---
title: Simplify configuration flags
description: Keep configuration flags, feature toggles, and build settings concise
  and well-organized. Use simpler names where appropriate and consolidate related
  flags when possible to improve readability and maintainability.
repository: tokio-rs/tokio
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 28989
---

Keep configuration flags, feature toggles, and build settings concise and well-organized. Use simpler names where appropriate and consolidate related flags when possible to improve readability and maintainability.

When defining new configuration flags:
- Choose concise, descriptive names without redundant prefixes
- Consider the context in which flags will be used
- Group related configuration options when possible

Example of simplifying multiple flags:
```diff
# Before: Multiple separate flags
- RUSTFLAGS: -Dwarnings --check-cfg=cfg(loom) --check-cfg=cfg(tokio_unstable) --check-cfg=cfg(tokio_taskdump) --check-cfg=cfg(fuzzing)

# After: Consolidated flags
+ RUSTFLAGS: -Dwarnings --check-cfg=cfg(loom, tokio_unstable, tokio_taskdump, fuzzing)
```

For feature flags and conditional compilation:
```diff
# Before: Verbose, redundant naming
- --cfg tokio_unstable_uring

# After: Simplified naming
+ --cfg tokio_uring
```

This approach makes configuration more maintainable, reduces verbosity, and improves readability, especially as the number of configuration options grows over time.