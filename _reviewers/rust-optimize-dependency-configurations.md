---
title: Optimize dependency configurations
description: 'When configuring project dependencies, be mindful of feature flags that
  may introduce unnecessary build dependencies or slow down compilation. For libraries
  like serde, separate the core functionality from derive macros to improve build
  parallelization:'
repository: rust-lang/rust
label: Configurations
language: Toml
comments_count: 2
repository_stars: 105254
---

When configuring project dependencies, be mindful of feature flags that may introduce unnecessary build dependencies or slow down compilation. For libraries like serde, separate the core functionality from derive macros to improve build parallelization:

```toml
# Preferred approach - separates core from proc macros
serde = "1.0.219"
serde_derive = "1.0.219"

# Instead of:
# serde = { version = "1.0.219", features = ["derive"] }
```

For tools and utilities that need to be lightweight, avoid heavy dependencies with proc-macro features when alternatives exist. Consider using builder APIs instead of derive-based approaches, or explicitly opt out of default features that aren't needed. This practice helps maintain fast build times and reduces the dependency footprint of your project.