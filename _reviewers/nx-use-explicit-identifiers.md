---
title: Use explicit identifiers
description: Choose explicit, unambiguous names for functions, variables, and parameters
  to avoid conflicts with common types and reduce reliance on implicit assumptions.
  Prefer descriptive names that clearly indicate purpose over generic terms that might
  be confused with built-in types or require string parsing.
repository: nrwl/nx
label: Naming Conventions
language: Rust
comments_count: 2
repository_stars: 27518
---

Choose explicit, unambiguous names for functions, variables, and parameters to avoid conflicts with common types and reduce reliance on implicit assumptions. Prefer descriptive names that clearly indicate purpose over generic terms that might be confused with built-in types or require string parsing.

For function names, avoid generic terms like `error` that commonly appear as type instances. Instead, use prefixed names like `log_error` or `logError` to clearly indicate the function's purpose.

For parameters, prefer explicit values over implicit extraction. Rather than parsing identifiers from formatted strings, pass the required values directly as separate parameters.

Example:
```rust
// Avoid: Generic name that conflicts with Error type
pub fn error(message: String) { ... }

// Prefer: Explicit, descriptive name
pub fn log_error(message: String) { ... }

// Avoid: Implicit extraction from formatted strings
let project_name = task_id.split(':').next().unwrap_or(task_id);

// Prefer: Explicit parameter passing
fn process_task(task_id: String, project_name: String) { ... }
```