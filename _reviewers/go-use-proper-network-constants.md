---
title: Use proper network constants
description: When writing network-related code, always use named constants from system
  packages instead of magic numbers, and ensure complete protocol implementation.
  This includes using proper constants for network operations (like `windows.IfOperStatusUp`
  instead of `0x01`), calculating buffer sizes correctly with system functions (like
  `syscall.CmsgSpace(4)` for file...
repository: golang/go
label: Networking
language: Go
comments_count: 6
repository_stars: 129599
---

When writing network-related code, always use named constants from system packages instead of magic numbers, and ensure complete protocol implementation. This includes using proper constants for network operations (like `windows.IfOperStatusUp` instead of `0x01`), calculating buffer sizes correctly with system functions (like `syscall.CmsgSpace(4)` for file descriptor passing), and setting absolute deadlines with `time.Now().Add()` rather than relative durations.

Additionally, avoid making assumptions about network infrastructure - for example, don't assume `req.TLS != nil` indicates HTTPS when TLS termination might occur at a load balancer. Always implement complete test scenarios that actually exercise the network paths being tested.

Example of proper constant usage:
```go
// Bad: magic number
if aa.OperStatus != 0x01 {
    continue
}

// Good: named constant  
if aa.OperStatus != windows.IfOperStatusUp {
    continue
}

// Bad: hardcoded buffer size
oob := make([]byte, 32)

// Good: calculated buffer size
oob := make([]byte, syscall.CmsgSpace(4))
```

This approach makes network code more maintainable, portable, and less prone to subtle bugs related to protocol assumptions or system-specific values.