---
title: Network information extraction
description: When extracting network information from connections (such as remote
  addresses, proxy IPs, or forwarded headers), implement robust extraction methods
  that don't depend on specific connection wrapper ordering or implementation details.
  Use iterative unwrapping patterns and ensure all relevant network information is
  properly preserved and forwarded.
repository: traefik/traefik
label: Networking
language: Go
comments_count: 4
repository_stars: 55772
---

When extracting network information from connections (such as remote addresses, proxy IPs, or forwarded headers), implement robust extraction methods that don't depend on specific connection wrapper ordering or implementation details. Use iterative unwrapping patterns and ensure all relevant network information is properly preserved and forwarded.

For proxy protocol handling, use a generic unwrapping approach:

```go
getProxyIP := func(c net.Conn) string {
    for {
        switch conn := c.(type) {
        case *tcprouter.Conn:
            c = conn.WriteCloser
        case *trackedConnection:
            c = conn.WriteCloser
        case *writeCloserWrapper:
            c = conn.writeCloser
        case *net.TCPConn:
            return c.RemoteAddr().String()
        default:
            return conn.RemoteAddr().String()
        }
    }
}
```

When forwarding HTTP requests, preserve all relevant network headers and use context values to pass network information between middleware layers:

```go
// Add back removed Forwarded Headers
req.Out.Header["Forwarded"] = req.In.Header["Forwarded"]
req.Out.Header["X-Forwarded-For"] = req.In.Header["X-Forwarded-For"]
req.Out.Header["X-Forwarded-Host"] = req.In.Header["X-Forwarded-Host"]
req.Out.Header["X-Forwarded-Proto"] = req.In.Header["X-Forwarded-Proto"]

// Use context values for network information
if xForwardedForAddr, ok := req.In.Context().Value(forwardedheaders.XForwardedForAddr).(string); ok {
    remoteAddr = xForwardedForAddr
}
```

This approach ensures network information remains accurate across different connection types and middleware layers, which is crucial for proper load balancing, health checking, and security features.