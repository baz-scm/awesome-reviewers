---
title: Platform-specific socket configuration
description: When configuring TCP socket options, always check the platform and apply
  appropriate settings for each operating system. Different platforms support different
  socket options and may require different approaches for connection management.
repository: commaai/openpilot
label: Networking
language: Python
comments_count: 2
repository_stars: 58214
---

When configuring TCP socket options, always check the platform and apply appropriate settings for each operating system. Different platforms support different socket options and may require different approaches for connection management.

Use proper platform detection with `sys.platform` to conditionally apply socket options. For example, `TCP_USER_TIMEOUT` is Linux-specific, while `TCP_KEEPALIVE` is used on Darwin (macOS). Always provide fallbacks or alternative approaches for unsupported platforms.

Example implementation:
```python
if sys.platform == 'linux':
  sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_USER_TIMEOUT, 16000 if onroad else 0)
  sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 7 if onroad else 30)
elif sys.platform == 'darwin':
  sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPALIVE, 7 if onroad else 30)
```

This approach ensures reliable network connections across different deployment environments and prevents runtime errors from unsupported socket operations. Consider the specific networking requirements of your application (timeouts, keepalive intervals) and how they should vary by platform and operational state.