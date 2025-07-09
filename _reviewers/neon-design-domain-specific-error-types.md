---
title: Design domain-specific error types
description: Create and use domain-specific error types instead of generic errors
  or anyhow. This improves error handling clarity and ensures proper error propagation
  through the codebase.
repository: neondatabase/neon
label: Error Handling
language: Rust
comments_count: 8
repository_stars: 19015
---

Create and use domain-specific error types instead of generic errors or anyhow. This improves error handling clarity and ensures proper error propagation through the codebase.

Key guidelines:
1. Define specific error types for your domain using enums
2. Include variants for different failure modes (e.g., Cancelled, ShuttingDown)
3. Provide clear, lowercase error messages with context
4. Propagate errors using proper type mapping

Example:

```rust
// Instead of using anyhow or generic errors:
fn process() -> anyhow::Result<()> {
    if cancelled {
        bail!("operation cancelled"); // Generic error
    }
    Ok(())
}

// Create domain-specific error types:
#[derive(Error, Debug)]
pub enum ProcessError {
    #[error("operation cancelled")]
    Cancelled,
    #[error("failed to write to {path}: {source}")]
    IoError { path: String, source: std::io::Error },
    #[error("invalid configuration: {0}")]
    Config(String),
}

fn process() -> Result<(), ProcessError> {
    if cancelled {
        return Err(ProcessError::Cancelled);
    }
    Ok(())
}

// Proper error mapping when crossing domain boundaries:
fn handle_process() -> Result<(), ApiError> {
    process().map_err(|e| match e {
        ProcessError::Cancelled => ApiError::ServiceUnavailable,
        ProcessError::IoError { .. } => ApiError::InternalError,
        ProcessError::Config(_) => ApiError::BadRequest,
    })?;
    Ok(())
}
```