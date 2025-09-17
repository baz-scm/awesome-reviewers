---
title: avoid error display duplication
description: When using thiserror for error handling, avoid displaying source errors
  in both the error message and the source attribute, as this creates duplicated error
  messages when printing the full error trace.
repository: unionlabs/union
label: Error Handling
language: Rust
comments_count: 3
repository_stars: 74800
---

When using thiserror for error handling, avoid displaying source errors in both the error message and the source attribute, as this creates duplicated error messages when printing the full error trace.

**The Problem:**
Using `#[from]` (which sets the source) while also including the error in the display message causes the same error to appear twice in error traces.

**Bad Example:**
```rust
#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error("database error creation transaction for dependency {0}: {1}")]
    CreateTransaction(AbiDependency, #[source] sqlx::Error),
}
```

**Good Examples:**
```rust
// Option 1: Use #[source] without displaying the error
#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error("database error creation transaction for dependency {0}")]
    CreateTransaction(AbiDependency, #[source] sqlx::Error),
}

// Option 2: Use #[from] for automatic conversion (implies #[source])
#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error("database error creation transaction for dependency {0}")]
    CreateTransaction(AbiDependency, #[from] sqlx::Error),
}

// Option 3: Use #[error(transparent)] to pass through the source error entirely
#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error(transparent)]
    Database(#[from] sqlx::Error),
}
```

**Key Rule:** Either set the source OR print it in display, but not both. The error chain will handle displaying source errors when the full trace is printed.