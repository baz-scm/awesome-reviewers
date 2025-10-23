---
title: avoid unsafe unwrapping
description: 'Replace `.unwrap()` calls and sentinel values with safe null handling
  patterns to prevent runtime panics and improve code robustness.


  **Key Issues:**'
repository: servo/servo
label: Null Handling
language: Rust
comments_count: 8
repository_stars: 32962
---

Replace `.unwrap()` calls and sentinel values with safe null handling patterns to prevent runtime panics and improve code robustness.

**Key Issues:**
1. **Unsafe unwrapping**: Using `.unwrap()` on operations that could fail, especially downcasts and IPC operations
2. **Sentinel values**: Using invalid constants like `Invalid` or `None = -1` instead of proper Option types
3. **Missing graceful degradation**: Not handling None cases appropriately

**Safe Patterns:**
- Use `if let Some(value) = optional_value` instead of `.unwrap()`
- Use `.expect("meaningful message")` when unwrapping is truly safe
- Replace sentinel values with `Option<T>` types
- Use `?` operator for early returns with Options
- Return `Option<T>` instead of default values when absence is meaningful

**Example:**
```rust
// ❌ Unsafe - could panic
let video_elem = self.downcast::<HTMLVideoElement>().unwrap();
video_elem.resize(width, height);

// ✅ Safe pattern
if let Some(video_elem) = self.downcast::<HTMLVideoElement>() {
    video_elem.resize(width, height);
}

// ❌ Sentinel value antipattern  
pub enum LargestContentfulPaintType {
    None = -1,
    // ...
}

// ✅ Proper Option usage
pub fn get_lcp_candidate() -> Option<LCPCandidate> {
    // ...
}
```

This prevents runtime crashes and makes null states explicit in the type system, improving both safety and code clarity.