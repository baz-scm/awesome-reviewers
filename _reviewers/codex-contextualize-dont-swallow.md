---
title: Contextualize, don't swallow
description: 'Always propagate errors with appropriate context rather than silently
  ignoring them. This makes debugging easier and prevents unexpected behavior.


  **Do**:'
repository: openai/codex
label: Error Handling
language: Rust
comments_count: 5
repository_stars: 31275
---

Always propagate errors with appropriate context rather than silently ignoring them. This makes debugging easier and prevents unexpected behavior.

**Do**:
- Return errors with added context using libraries like `anyhow`
- Use `.context()` or `.with_context()` to explain what operation failed
- Make intentional decisions about when to recover vs. when to fail fast

**Don't**:
- Silently ignore errors, especially for I/O operations
- Swallow critical dependency failures
- Use `.expect()` or `.unwrap()` in production code

**Example - Bad**:
```rust
// Silently ignoring errors
parser.set_language(&lang).expect("load bash grammar");

// Ignoring I/O errors
async fn rollout_writer(...) {
    if let Some(meta) = meta {
        // I/O errors ignored here
    }
}
```

**Example - Good**:
```rust
// Adding context to errors
parser
    .set_language(&lang)
    .context("failed to load bash grammar")?;

// Properly handling utf8 conversion errors
let text = node
    .utf8_text(bytes)
    .map_err(|e| anyhow::anyhow!("failed to interpret heredoc body as UTF-8: {e}"))?;

// Properly propagating I/O errors
async fn rollout_writer(...) -> std::io::Result<()> {
    if let Some(meta) = meta {
        // Return I/O errors
    }
    Ok(())
}
```

Critical system dependencies failing should cause immediate failure rather than silent recovery. For common error patterns, consider creating utility functions that handle errors consistently.