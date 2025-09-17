---
title: explicit error handling
description: Avoid catch-all patterns and implicit error handling. Handle each error
  case explicitly, use the ? operator for error propagation instead of explicit returns,
  and never silently ignore errors.
repository: juspay/hyperswitch
label: Error Handling
language: Rust
comments_count: 11
repository_stars: 34028
---

Avoid catch-all patterns and implicit error handling. Handle each error case explicitly, use the ? operator for error propagation instead of explicit returns, and never silently ignore errors.

Key practices:
- Replace wildcard patterns (`_`, `unwrap_or_default()`) with explicit case handling
- Use `?` operator instead of `return Err(...)` for consistent error propagation  
- Log errors even when continuing execution, don't silently ignore failures
- Provide meaningful error context with `attach_printable()` or `change_context()`

Example of problematic patterns:
```rust
// Avoid catch-all wildcards
match capture_method {
    Some(CaptureMethod::Manual) => Status::Authorized,
    _ => Status::Charged,  // Too broad, handle each case explicitly
}

// Avoid explicit returns
if error.is_some() {
    return Err(SomeError);  // Use ? operator instead
}

// Avoid silent error handling
match result {
    Ok(value) => value,
    Err(_) => {} // Log the error at minimum
}
```

Better approach:
```rust
match capture_method {
    Some(CaptureMethod::Manual) => Status::Authorized,
    Some(CaptureMethod::Automatic) => Status::Charged,
    Some(unsupported) => return Err(UnsupportedCaptureMethod(unsupported)),
    None => return Err(MissingCaptureMethod),
}

// Use ? for error propagation
let result = operation().change_context(MyError::OperationFailed)?;

// Always handle errors meaningfully
match result {
    Ok(value) => value,
    Err(e) => {
        logger::error!("Operation failed: {:?}", e);
        return Err(e);
    }
}
```