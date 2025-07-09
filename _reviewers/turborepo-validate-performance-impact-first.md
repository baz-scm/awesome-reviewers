---
title: Validate performance impact first
description: 'Always validate performance changes through profiling or benchmarking
  before implementation, and favor memory-efficient patterns when making optimizations.
  Key practices:'
repository: vercel/turborepo
label: Performance Optimization
language: Rust
comments_count: 5
repository_stars: 28115
---

Always validate performance changes through profiling or benchmarking before implementation, and favor memory-efficient patterns when making optimizations. Key practices:

1. Profile before/after significant changes:
```rust
// Before changing buffer sizes, validate impact:
const SCROLLBACK_LEN: usize = 1024;
// Profile current performance
// Test new value
const SCROLLBACK_LEN: usize = 2048;
// Validate no significant regression
```

2. Use memory-efficient patterns:
- Prefer `&str` over `&String` to avoid double indirection
- Initialize collections with capacity when size is known:
  ```rust
  let mut map = HashMap::with_capacity(items.len());
  ```
- Return iterators instead of collecting vectors when possible:
  ```rust
  // Instead of
  pub fn get_items(&self) -> Vec<String> {
      self.items.iter().map(|i| i.to_string()).collect()
  }
  // Prefer
  pub fn get_items(&self) -> impl Iterator<Item = &str> + '_ {
      self.items.iter().map(|i| i.as_str())
  }
  ```

3. Document performance-critical decisions with benchmarks or profiling results to justify changes.