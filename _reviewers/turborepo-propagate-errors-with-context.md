---
title: Propagate errors with context
description: Properly propagate errors to callers with sufficient context rather than
  handling them prematurely or hiding them. Let the caller decide how to handle errors
  when they have the appropriate context.
repository: vercel/turborepo
label: Error Handling
language: Rust
comments_count: 9
repository_stars: 28115
---

Properly propagate errors to callers with sufficient context rather than handling them prematurely or hiding them. Let the caller decide how to handle errors when they have the appropriate context.

**Do:**
- Use the `?` operator to bubble up errors to callers
- Add context to errors when propagating them
- Use custom error types with `#[from]` for clean error conversion
- Include specific details in error messages that help users understand the issue

```rust
// Good: Propagate error with context
pub async fn run(base: CommandBase) -> Result<(), Error> {
    match info::run(base).await {
        Ok(()) => Ok(()),
        Err(e) => Err(Error::Info(e)) // With #[from] annotation on Error::Info
    }
}

// Good: Preserve error details
let exe_path = std::env::current_exe().map_or_else(
    |e| format!("Cannot determine current binary: {e}"),
    |p| p.display().to_string()
);

// Good: Use methods that include context in errors
preferences_file.ensure_dir()?; // Path information included in error
```

**Don't:**
- Use lossy conversions that cause silent failures
- Handle errors locally when the caller needs to make decisions
- Use generic error messages that hide important details
- Use `.unwrap()` or `.expect()` in production code paths unless failure is truly impossible

```rust
// Bad: Lossy conversion causing silent failures
let stdout = String::from_utf8_lossy(&stdout);

// Bad: Using unwrap which hides error context
let anchored_to_turbo_root_file_path = self
    .reanchor_path_from_git_root_to_turbo_root(turbo_root, path)
    .unwrap();
```

Only handle errors locally when you have sufficient context to make the right decision; otherwise, propagate them with as much information as possible.