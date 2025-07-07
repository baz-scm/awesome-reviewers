---
title: Handle nullable types idiomatically
description: "Use Rust's idiomatic patterns when working with Option and Result types\
  \ to prevent panics and improve code clarity. \n\n**Avoid unwrapping**\nPrefer pattern\
  \ matching or propagating errors instead of using `.unwrap()` which can cause runtime\
  \ panics:"
repository: huggingface/tokenizers
label: Null Handling
language: Rust
comments_count: 5
repository_stars: 9868
---

Use Rust's idiomatic patterns when working with Option and Result types to prevent panics and improve code clarity. 

**Avoid unwrapping**
Prefer pattern matching or propagating errors instead of using `.unwrap()` which can cause runtime panics:

```rust
// Instead of this:
fn __str__(&self) -> PyResult<String> {
    Ok(format!("{}", self.model.read().unwrap()))
}

// Prefer this:
fn __str__(&self) -> PyResult<String> {
    self.model.read()
        .map(|model| format!("{}", model))
        .map_err(|e| e.into()) // Convert to PyResult
}
```

**Use Option types appropriately**
Only use Option<T> when a value can truly be absent. For boolean flags, use bool instead of Option<bool> unless "no preference" is truly needed:

```rust
// Instead of:
pub fn from(
    vocab: Vec<(String, f64)>,
    unk_id: Option<usize>,
    byte_fallback: Option<bool>, // Unnecessarily complex
) -> Result<Self>

// Prefer:
pub fn from(
    vocab: Vec<(String, f64)>,
    unk_id: Option<usize>, // Truly optional
    byte_fallback: bool,    // Just a flag
) -> Result<Self>
```

**Handle Option values clearly**
Use clear patterns for handling optional values, remembering that None means absence, not zero:

```rust
// Instead of:
match max_merge_length {
    None | Some(0) => { /* in case 0 was manually entered, treat as None */ }
    Some(length) => { /* handle length */ }
}

// Prefer:
if let Some(max_token_length) = max_token_length {
    if new_token.chars().count() > max_token_length {
        continue;
    }
}
```

**Design for nullable parameters**
When creating APIs with optional parameters, consider how values can be both set and unset:

```rust
// Option in builder pattern
fn with_dropout(mut self, dropout: Option<f32>) -> Self {
    self.dropout = dropout;
    self
}

// Or provide explicit methods
fn with_dropout(mut self, dropout: f32) -> Self {
    self.dropout = Some(dropout);
    self
}

fn without_dropout(mut self) -> Self {
    self.dropout = None;
    self
}
```