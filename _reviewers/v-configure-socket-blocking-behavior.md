---
title: Configure socket blocking behavior
description: Always explicitly configure socket blocking behavior when creating TCP
  connections, and provide compile-time flags for backwards compatibility when changing
  default behaviors.
repository: vlang/v
label: Networking
language: Other
comments_count: 4
repository_stars: 36582
---

Always explicitly configure socket blocking behavior when creating TCP connections, and provide compile-time flags for backwards compatibility when changing default behaviors.

When establishing TCP connections, don't rely on implicit socket blocking settings. Instead, explicitly set the blocking mode after connection creation. When changing default socket behavior, use compile-time conditional compilation to allow users to opt into the previous behavior if needed.

Example implementation:
```v
mut conn := &TcpConn{
    sock: s
    read_timeout: net.tcp_default_read_timeout
    write_timeout: net.tcp_default_write_timeout
}
$if !net_nonblocking_sockets ? {
    conn.set_blocking(true)!
}
```

This pattern ensures that:
- Socket blocking behavior is explicit and predictable
- Default behavior changes don't break existing code
- Users can opt into non-blocking sockets when needed via `-d net_nonblocking_sockets`
- The code is self-documenting about its networking assumptions

Apply this approach consistently across all TCP connection creation points including `dial_tcp()`, `dial_tcp_with_bind()`, and `TcpListener.accept()`.