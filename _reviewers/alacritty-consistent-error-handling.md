---
title: consistent error handling
description: Maintain uniform error handling patterns throughout the codebase. Avoid
  mixing different error handling approaches like panics, process::exit(), and proper
  Result returns within the same application flow.
repository: alacritty/alacritty
label: Error Handling
language: Rust
comments_count: 4
repository_stars: 59675
---

Maintain uniform error handling patterns throughout the codebase. Avoid mixing different error handling approaches like panics, process::exit(), and proper Result returns within the same application flow.

When functions can fail, consistently use Result types and propagate errors up the call stack rather than handling them inconsistently at different levels. This makes error handling predictable and allows callers to decide how to respond to failures.

Example of inconsistent handling to avoid:
```rust
// Bad: mixing panic and proper error handling
pub fn migrate(options: MigrateOptions) {
    if let Err(e) = some_operation() {
        eprintln!("Error: {}", e);
        process::exit(1);  // Inconsistent with other subcommands
    }
}

// Good: consistent Result-based error handling
pub fn migrate(options: MigrateOptions) -> Result<(), Box<dyn Error>> {
    some_operation()?;  // Propagate errors consistently
    Ok(())
}
```

Instead of using panics for error conditions, return proper error types with span information when possible. This is especially important for compile-time errors and user-facing operations where graceful degradation is preferred over abrupt termination.

The goal is to make error handling predictable across the entire codebase, allowing for better testing, debugging, and user experience.