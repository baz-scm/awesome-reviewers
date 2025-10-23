---
title: Handle unsafe code properly
description: Methods that access raw memory buffers, perform pointer operations, or
  interact with foreign function interfaces must be explicitly marked as `unsafe`
  to prevent memory safety vulnerabilities. Conversely, remove unnecessary `unsafe`
  blocks when calling safe functions to maintain code clarity and prevent masking
  actual unsafe operations.
repository: servo/servo
label: Security
language: Rust
comments_count: 3
repository_stars: 32962
---

Methods that access raw memory buffers, perform pointer operations, or interact with foreign function interfaces must be explicitly marked as `unsafe` to prevent memory safety vulnerabilities. Conversely, remove unnecessary `unsafe` blocks when calling safe functions to maintain code clarity and prevent masking actual unsafe operations.

Key principles:
- Mark methods `unsafe` when they access raw memory that could be invalidated (e.g., borrowed string buffers that could be freed)
- Avoid `transmute` operations that create technical debt and potential memory safety issues during library upgrades
- Remove `unsafe` blocks when the called functions are actually safe

Example of proper unsafe marking:
```rust
// BAD: Missing unsafe marker for dangerous operation
pub(super) fn bytes<'a>(&'a self) -> EncodedBytes<'a> {
    // Accesses raw JS string buffer that could be invalidated
}

// GOOD: Properly marked as unsafe
pub(super) unsafe fn bytes<'a>(&'a self) -> EncodedBytes<'a> {
    // Caller must ensure JS string won't be mutated/freed
}

// BAD: Unnecessary unsafe block
unsafe { root_from_handlevalue::<TrustedScriptURL>(value, cx).is_ok() }

// GOOD: Remove unsafe when function is safe
root_from_handlevalue::<TrustedScriptURL>(value, cx).is_ok()
```

This prevents memory corruption vulnerabilities and maintains Rust's memory safety guarantees while clearly communicating risk to API consumers.