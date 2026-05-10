---
title: Manage network resources
description: 'When working with streaming or TCP options, be explicit and defensive:


  1) Closing streams: If you terminate a stream early (e.g., you don’t fully consume
  an HTTP/SSE iterator), ensure you close the underlying network resource—not just
  a wrapper/decoder that may not implement `close()`.'
repository: anthropics/anthropic-sdk-python
label: Networking
language: Python
comments_count: 2
repository_stars: 3392
---

When working with streaming or TCP options, be explicit and defensive:

1) Closing streams: If you terminate a stream early (e.g., you don’t fully consume an HTTP/SSE iterator), ensure you close the underlying network resource—not just a wrapper/decoder that may not implement `close()`.

2) Socket options: Set keepalive (and similar socket options) only when the platform exposes the needed constants, and use mutually exclusive conditionals to avoid configuring conflicting options.

Example pattern:

```python
# 1) Stream termination: close the underlying response/connection
try:
    # consume partially or stop early
    ...
finally:
    # Prefer the actual HTTP response/connection close
    if hasattr(response, "close"):
        response.close()
    elif hasattr(decoder, "close"):
        decoder.close()

# 2) TCP keepalive: conditional and non-conflicting configuration
socket_options = [(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)]
TCP_KEEPINTVL = getattr(socket, "TCP_KEEPINTVL", None)

if TCP_KEEPINTVL is not None:
    socket_options.append((socket.IPPROTO_TCP, TCP_KEEPINTVL, 60))
elif sys.platform == "darwin":
    TCP_KEEPALIVE = getattr(socket, "TCP_KEEPALIVE", None)
    if TCP_KEEPALIVE is not None:
        socket_options.append((socket.IPPROTO_TCP, TCP_KEEPALIVE, 60))
```

Apply this standard to prevent leaked connections, hanging sockets, and platform-specific networking bugs.