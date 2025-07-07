---
title: Precompute over recalculate
description: Perform expensive calculations during initialization rather than on each
  request, and avoid unnecessary operations in frequently executed code paths. This
  significantly improves performance in high-traffic applications.
repository: gin-gonic/gin
label: Performance Optimization
language: Go
comments_count: 3
repository_stars: 83022
---

Perform expensive calculations during initialization rather than on each request, and avoid unnecessary operations in frequently executed code paths. This significantly improves performance in high-traffic applications.

Key practices:
- Cache computed values that don't change between requests
- Avoid redundant parsing operations on each request
- Eliminate unnecessary pointer operations in hot paths

Example:
```go
// Instead of this:
func (c *Context) ClientIP() string {
    // Parse trusted proxies on every request
    for _, trustedProxy := range e.TrustedProxies {
        // Parse CIDR each time
    }
    return ip
}

// Do this:
type Engine struct {
    // Precomputed during initialization
    trustedCIDR []*net.IPNet
    // ...
}

func (e *Engine) Run() {
    // Precompute once during startup
    e.trustedCIDR = parseTrustedProxies(e.TrustedProxies)
    // ...
}

func (c *Context) ClientIP() string {
    // Use precomputed values
    return ip
}
```

Similarly, for operations like BSON marshaling, avoid unnecessary pointer indirection:
```go
// Prefer this when possible:
bytes, err := bson.Marshal(r.Data)

// Over this:
bytes, err := bson.Marshal(&r.Data)
```