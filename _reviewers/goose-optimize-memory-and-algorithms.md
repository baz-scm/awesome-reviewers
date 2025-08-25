---
title: Optimize memory and algorithms
description: 'Focus on efficient memory usage and algorithm selection while preserving
  functionality. Apply these optimization techniques:


  **Memory optimization:**'
repository: block/goose
label: Performance Optimization
language: Rust
comments_count: 4
repository_stars: 19037
---

Focus on efficient memory usage and algorithm selection while preserving functionality. Apply these optimization techniques:

**Memory optimization:**
- Use conservative default values for memory-intensive constants (prefer ~5k over 50k for buffers)
- Pre-allocate collections when the final size is known: `Vec::with_capacity(known_size)`
- Avoid unnecessary intermediate collections by using direct operations

**Algorithm efficiency:**
- Use direct slicing instead of collecting intermediate vectors:
```rust
// Instead of: lines.iter().rev().take(100).rev().copied().collect()
let start = lines.len().saturating_sub(100);
let result = lines[start..].join("\n");
```
- Prefer efficient data structure operations like HashMap membership tests over string prefix matching:
```rust
// Instead of: tool_name.starts_with(PREFIX)
// Use: self.tool_map.contains_key(tool_name)
```

Remember that correctness takes priority over performance optimizations. Avoid truncating or modifying data in ways that could break downstream functionality, even if it improves performance metrics.