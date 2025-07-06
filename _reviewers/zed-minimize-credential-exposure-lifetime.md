---
title: Minimize credential exposure lifetime
description: 'Credentials and secrets should never be stored persistently in memory
  or written to files. Instead, use ephemeral patterns that limit the lifetime of
  sensitive data:'
repository: zed-industries/zed
label: Security
language: Rust
comments_count: 2
repository_stars: 62119
---

Credentials and secrets should never be stored persistently in memory or written to files. Instead, use ephemeral patterns that limit the lifetime of sensitive data:

1. Use one-time channels or receivers to pass credentials only when needed
2. Immediately consume credentials rather than storing them in struct fields
3. Ensure sensitive data is properly cleared/dropped after use

Example of a problematic pattern:
```rust
pub struct AskPassSession {
    askpass_helper: String,
    _askpass_task: Task<()>,
    secret: std::sync::Arc<std::sync::Mutex<String>>, // Stores credential persistently
}
```

Better pattern:
```rust
// Create a one-time channel for the credential
let (askpass, askpass_rx) = create_oneshot_channel();

// Use the credential only when needed
let Some(password) = askpass_rx.next().await else { /* handle error */ };
let socket = SshSocket::new(connection_options, &temp_dir, password)?;

// Password is consumed and doesn't persist in memory
```

This approach ensures credentials exist in memory only for the minimum time necessary and reduces the security risk if the application memory is compromised.