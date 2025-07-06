---
title: Contextualize don't panic
description: Always provide meaningful context for errors and avoid code that can
  panic in production. Use `.context()` or `.with_context()` to add rich error information,
  making debugging easier. Replace `.unwrap()` and `.expect()` with proper error handling
  mechanisms like error propagation or logging.
repository: zed-industries/zed
label: Error Handling
language: Rust
comments_count: 4
repository_stars: 62119
---

Always provide meaningful context for errors and avoid code that can panic in production. Use `.context()` or `.with_context()` to add rich error information, making debugging easier. Replace `.unwrap()` and `.expect()` with proper error handling mechanisms like error propagation or logging.

Example - Poor error handling:
```rust
// No context added to errors
fs::write(&askpass_script_path, askpass_script).await?;

// Potential panics in production
let file_path = python_extract_path_and_line(file_line.as_str())
    .expect("Cannot parse python file line syntax");
```

Example - Better error handling:
```rust
// Rich context added to errors
fs::write(&askpass_script_path, askpass_script)
    .await
    .with_context(|| format!("Creating askpass script at {askpass_script_path:?}"))?;

// No panic risk, proper error propagation
let file_path = match python_extract_path_and_line(file_line.as_str()) {
    Some(result) => result,
    None => {
        log::warn!("Failed to parse Python file line syntax: {}", file_line);
        return None;
    }
};
```

For error handling in library code, preserve full error information rather than simplifying too early (e.g., prefer returning `Result` over `Option` when information might be useful). When handling errors that shouldn't propagate, use `.log_err()` rather than silently discarding them with `let _`.