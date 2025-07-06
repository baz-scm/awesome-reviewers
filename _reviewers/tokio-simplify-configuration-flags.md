---
title: Simplify configuration flags
description: Use concise, meaningful names for configuration flags and consolidate
  related flags when possible to improve readability and maintainability. Avoid overly
  verbose or nested naming patterns when a simpler alternative conveys the same information.
repository: tokio-rs/tokio
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 28981
---

Use concise, meaningful names for configuration flags and consolidate related flags when possible to improve readability and maintainability. Avoid overly verbose or nested naming patterns when a simpler alternative conveys the same information.

For example, instead of:
```
RUSTFLAGS: -Dwarnings --check-cfg=cfg(loom) --check-cfg=cfg(tokio_unstable) --check-cfg=cfg(tokio_taskdump) --check-cfg=cfg(fuzzing) --check-cfg=cfg(mio_unsupported_force_poll_poll)
```

Prefer:
```
RUSTFLAGS: -Dwarnings --check-cfg=cfg(loom, tokio_unstable, tokio_taskdump, fuzzing, mio_unsupported_force_poll_poll)
```

Similarly, prefer simplified flag names like `tokio_uring` over more complex variants like `tokio_unstable_uring` when the additional qualification doesn't provide meaningful context. This principle applies to all configuration elements: feature flags, environment variables, and command line arguments.