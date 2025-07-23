---
title: Explicit security bypass
description: When implementing functionality to bypass security controls (like sandboxing),
  ensure the bypass is complete and explicit rather than just configuring existing
  security mechanisms to be permissive. Create dedicated code paths for unrestricted
  operation that truly bypass all security layers.
repository: openai/codex
label: Security
language: Rust
comments_count: 1
repository_stars: 31275
---

When implementing functionality to bypass security controls (like sandboxing), ensure the bypass is complete and explicit rather than just configuring existing security mechanisms to be permissive. Create dedicated code paths for unrestricted operation that truly bypass all security layers.

For example, instead of:
```rust
pub fn new_unrestricted_policy() -> Self {
    // This still uses the sandbox with relaxed permissions
    SandboxPolicy {
        allow_disk_read: true,
        allow_disk_write: true,
        allow_network: true,
        auto_approve: true,
    }
}
```

Implement a truly separate path:
```rust
pub fn new_unrestricted_policy() -> Self {
    // Explicitly use NoSandbox implementation
    SandboxPolicy {
        sandbox_type: SandboxType::NoSandbox,
        // other fields as needed
    }
}
```

This prevents subtle security issues where sandboxing mechanisms might still be partially active despite intending to fully bypass them.