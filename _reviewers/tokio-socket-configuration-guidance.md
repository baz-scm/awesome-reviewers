---
title: Socket configuration guidance
description: When implementing networking APIs, always clearly document socket modes,
  configuration options, and platform-specific behaviors. Be explicit about blocking
  versus non-blocking mode implications, required flags, and ensure consistent API
  design across related components.
repository: tokio-rs/tokio
label: Networking
language: Rust
comments_count: 5
repository_stars: 28981
---

When implementing networking APIs, always clearly document socket modes, configuration options, and platform-specific behaviors. Be explicit about blocking versus non-blocking mode implications, required flags, and ensure consistent API design across related components.

For socket modes, provide explicit warnings about incorrect configurations:

```rust
/// Create a new listener from a standard library socket.
///
/// Warning: Passing a listener in blocking mode is erroneous, and the
/// behavior in that case may change in the future. For example, it could panic.
pub fn from_std(socket: std::net::TcpListener) -> io::Result<TcpListener> {
    // Implementation...
}
```

When exposing low-level socket options, document flag requirements and constraints:

```rust
/// Create a new AsyncFd with the provided raw epoll flags for registration.
///
/// These flags replace any epoll flags would normally set when registering the fd.
/// Note that `EPOLLONESHOT` must not be used, and `EPOLLET` must be set.
///
/// **Note**: This is an [unstable API][unstable]. The public API of this may 
/// break in 1.x releases.
#[cfg(all(target_os = "linux", tokio_unstable))]
pub fn with_epoll_flags(inner: T, flags: u32) -> io::Result<Self>
```

For platform-specific features, include appropriate conditional compilation and clear handling:

```rust
// Properly handle platform-specific socket behaviors
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

Maintain consistent APIs when adding socket configuration methods, carefully handling type conversions when needed:

```rust
/// Sets the size of the UDP send buffer on this socket.
///
/// On most operating systems, this sets the `SO_SNDBUF` socket option.
pub fn set_send_buffer_size(&self, size: u32) -> io::Result<()> {
    self.to_socket().set_send_buffer_size(size as usize)
}
```