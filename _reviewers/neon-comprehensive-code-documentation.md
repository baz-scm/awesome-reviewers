---
title: Comprehensive code documentation
description: 'Properly document code with clear, accurate, and useful comments using
  the correct syntax based on context:


  1. Use `///` to document items (structs, functions, etc.) that follow the comment:'
repository: neondatabase/neon
label: Documentation
language: Rust
comments_count: 5
repository_stars: 19015
---

Properly document code with clear, accurate, and useful comments using the correct syntax based on context:

1. Use `///` to document items (structs, functions, etc.) that follow the comment:
```rust
/// Struct to store runtime state of the compute monitor thread.
/// Handles tracking Postgres availability and managing downtime metrics.
pub struct ComputeMonitor {
    // ...
}
```

2. Use `//!` for module or crate-level documentation that applies to the enclosing item.

3. Document all public structures, traits, and functions with explanations of:
   - Their purpose
   - Usage considerations
   - Potential pitfalls or caveats

4. For complex data structures, include explanations of fields and their relationships:
```rust
/// Range of LSNs for page requests
/// - request_lsn: LSN specifically requested by compute
/// - effective_lsn: LSN actually used for the request (may differ from request_lsn)
/// Note: Primary computes typically use request_lsn == MAX
pub struct LsnRange {
    pub request_lsn: Lsn,
    pub effective_lsn: Lsn,
}
```

5. Ensure comments are accurate and up-to-date. Never merge incorrect comments with the intention to fix them later.

6. When referencing other code elements, use proper linking syntax: `[`Type::method()`]` to enable IDE navigation.

7. Avoid redundant comments that merely restate what is already clear from the code or function names.

Good documentation serves as both a reference for users of your code and as context for future developers (including yourself) who will need to maintain it.