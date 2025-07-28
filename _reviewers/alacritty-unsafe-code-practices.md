---
title: unsafe code practices
description: Ensure proper use and documentation of unsafe code to prevent security
  vulnerabilities. The `unsafe` keyword should only be used for operations that can
  violate memory safety contracts, not for general thread safety or global state concerns.
  All unsafe functions must include comprehensive safety documentation explaining
  the contracts that callers must...
repository: alacritty/alacritty
label: Security
language: Rust
comments_count: 2
repository_stars: 59675
---

Ensure proper use and documentation of unsafe code to prevent security vulnerabilities. The `unsafe` keyword should only be used for operations that can violate memory safety contracts, not for general thread safety or global state concerns. All unsafe functions must include comprehensive safety documentation explaining the contracts that callers must uphold.

When marking code as unsafe:
- Only use `unsafe` for true memory safety violations (e.g., raw pointer dereferencing, FFI calls)
- Do NOT use `unsafe` for thread safety issues or global state mutations that use safe Rust APIs
- Always document safety requirements with `/// # Safety` comments

Example of proper unsafe documentation:
```rust
/// # Safety
///
/// The underlying sources must outlive their registration in the `Poller`.
unsafe fn register(&mut self, poller: &Arc<Poller>, event: Event, mode: PollMode) -> io::Result<()>;
```

Example of improper unsafe usage:
```rust
// WRONG: This just calls std::env::remove_var, which is safe
unsafe fn reset_activation_token_env() {
    std::env::remove_var("DESKTOP_STARTUP_ID");
}
```

Thread safety and global state concerns should be addressed through proper synchronization primitives (Mutex, RwLock) rather than marking functions as unsafe.