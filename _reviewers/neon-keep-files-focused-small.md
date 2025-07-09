---
title: Keep files focused small
description: Maintain code organization by keeping files focused on a single responsibility
  and splitting large files into smaller, well-organized modules. This improves code
  navigation, readability, and maintainability.
repository: neondatabase/neon
label: Code Style
language: Rust
comments_count: 6
repository_stars: 19015
---

Maintain code organization by keeping files focused on a single responsibility and splitting large files into smaller, well-organized modules. This improves code navigation, readability, and maintainability.

Key guidelines:
1. Move code to dedicated files when it represents a distinct functionality
2. Split large files (>500 lines) into logical modules
3. Place related functionality in the same module
4. Use clear, descriptive file names that reflect the content

Example of good organization:
```rust
// Instead of putting everything in mod.rs:
// src/binary/mod.rs
mod local_proxy;  // Move to separate file
pub use local_proxy::*;

// src/binary/local_proxy.rs
pub struct LocalProxy {
    // Implementation details
}

// Instead of one large compute.rs:
// src/compute/mod.rs
mod core;        // Core compute functionality
mod prewarm;     // Prewarm-specific implementations
mod helpers;     // Helper functions

pub use core::ComputeNode;
```

This approach:
- Makes code easier to navigate and maintain
- Reduces cognitive load when working with the codebase
- Facilitates code review and testing
- Improves module cohesion