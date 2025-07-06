---
title: Network API design consistency
description: 'When designing networking APIs, maintain consistency with existing interfaces
  while ensuring proper cross-platform compatibility. Follow these key principles:'
repository: tokio-rs/tokio
label: Networking
language: Rust
comments_count: 6
repository_stars: 28989
---

When designing networking APIs, maintain consistency with existing interfaces while ensuring proper cross-platform compatibility. Follow these key principles:

1. **Type consistency**: Use consistent types across related APIs. If existing APIs use specific types (like `u32` for buffer sizes), maintain this pattern even if underlying libraries use different types.

```rust
// Good - matches existing TcpSocket API pattern
pub fn set_send_buffer_size(&self, size: u32) -> io::Result<()> {
    self.to_socket().set_send_buffer_size(size as usize)
}
```

2. **Platform-specific handling**: Explicitly handle platform-specific features with clear conditional compilation and documentation.

```rust
#[cfg(any(target_os = "linux", target_os = "android"))]
let addr = {
    let os_str_bytes = path.as_ref().as_os_str().as_bytes();
    if os_str_bytes.starts_with(b"\0") {
        StdSocketAddr::from_abstract_name(os_str_bytes)?
    } else {
        StdSocketAddr::from_pathname(path)?
    }
};
```

3. **Abstraction boundaries**: Consider whether low-level system calls should be exposed directly or via higher-level abstractions. When bypassing abstractions (like Mio), document the implications and ensure future compatibility.

4. **Document constraints**: When exposing low-level features like epoll flags, clearly document requirements and add debug assertions.

```rust
/// Create a new AsyncFd with the provided raw epoll flags for registration.
///
/// These flags replace any epoll flags would normally set when registering the fd.
/// Note that `EPOLLONESHOT` must not be used, and `EPOLLET` must be set.
```

5. **Implementation correctness**: For functions that check resource states like terminals, avoid implementations that can produce incorrect results during ongoing operations.

```rust
// Good - direct access ensures correct result even during I/O operations
pub fn is_terminal(&self) -> bool {
    std::io::stderr().is_terminal()
}
```

By following these principles, you'll create networking APIs that are consistent, reliable across platforms, and easier for users to understand and use correctly.