---
title: Robust network handling
description: Always implement proper network timeout handling and address formatting
  to ensure robust connectivity across different network conditions and IP protocols.
repository: vitessio/vitess
label: Networking
language: Go
comments_count: 3
repository_stars: 19815
---

Always implement proper network timeout handling and address formatting to ensure robust connectivity across different network conditions and IP protocols.

**Timeouts:**
- Use explicit timeouts for all network operations rather than relying on indefinite waits
- Leverage existing timeout constants (like `RemoteOperationTimeout`) instead of hardcoding arbitrary values
- Pass timeout parameters explicitly to connection operations

**Address formatting:**
- Use `net.JoinHostPort()` when combining host and port values to ensure compatibility with both IPv4 and IPv6
- Be explicit about network binding addresses and understand the implications (127.0.0.1 for localhost-only vs 0.0.0.0 for all interfaces)

Example of proper implementation:

```go
// GOOD: Using proper timeout and address formatting
ctx, cancel := context.WithTimeout(context.Background(), config.RemoteOperationTimeout)
defer cancel()

// Using net.JoinHostPort for proper IPv4/IPv6 handling
address := net.JoinHostPort(host, port) 
conn, err := grpc.DialContext(ctx, address, grpc.WithBlock())

// BAD: Hardcoded timeout and manual address formatting
ctx, cancel := context.WithTimeout(context.Background(), 15*time.Second)
defer cancel()

// Manual concatenation doesn't handle IPv6 properly
address := host + ":" + port
conn, err := grpc.DialContext(ctx, address, grpc.WithBlock())
```

This approach prevents connection hangs during network issues while ensuring compatibility across IP protocol versions.