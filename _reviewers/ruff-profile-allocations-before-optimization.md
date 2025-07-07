---
title: Profile allocations before optimization
description: 'Before implementing data structures or algorithms, analyze allocation
  patterns and optimize for common cases. Key strategies:


  1. Use fixed-size arrays for known small collections:'
repository: astral-sh/ruff
label: Performance Optimization
language: Rust
comments_count: 5
repository_stars: 40619
---

Before implementing data structures or algorithms, analyze allocation patterns and optimize for common cases. Key strategies:

1. Use fixed-size arrays for known small collections:
```rust
// Before
pub fn all() -> Vec<&'static str> {
    vec!["namespace", "class", ...]
}

// After
pub const fn all() -> [&'static str; 15] {
    ["namespace", "class", ...]
}
```

2. Leverage specialized data structures to avoid allocations:
- Use `hashbrown::HashMap` with `entry_ref` for string keys
- Consider `smallvec` for collections that are usually small
- Keep allocations behind `Arc` when possible

3. Profile before optimizing:
- Measure binary size impact of changes
- Use tools like cargo-bloat to identify hot spots
- Consider both debug and release mode implications

The goal is to minimize allocations in hot paths while keeping code maintainable. Always validate optimizations with benchmarks and profiles.