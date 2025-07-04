---
title: Background process blocking operations
description: 'Always move potentially blocking operations to background threads to
  maintain UI responsiveness. Use appropriate spawning mechanisms based on the operation
  type:'
repository: zed-industries/zed
label: Concurrency
language: Rust
comments_count: 4
repository_stars: 62119
---

Always move potentially blocking operations to background threads to maintain UI responsiveness. Use appropriate spawning mechanisms based on the operation type:

1. For CPU-intensive work or file operations:
```rust
// Don't do this - blocks main thread
let result = heavy_computation();

// Do this instead
cx.background_spawn(async move {
    let result = heavy_computation();
    // Update state after computation
}).await;
```

2. For state updates after background work:
```rust
// Accumulate new state first
let new_state = cx.background_spawn(async move {
    let mut new_data = Vec::new();
    // ... heavy computation ...
    new_data
}).await;

// Then update actual state once
self.state = new_state;
```

Key principles:
- Use cx.background_spawn() for CPU-intensive operations
- Keep main thread operations light and UI-focused
- Accumulate state changes in background before applying
- Consider using rate limits for multiple concurrent operations

This pattern is essential for maintaining application responsiveness and preventing UI freezes.