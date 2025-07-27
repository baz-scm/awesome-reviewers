---
title: API interface design
description: Design interfaces that balance simplicity with extensibility. Consolidate
  related parameters into cohesive data structures to reduce interface complexity,
  while using interfaces to enable future implementations and maintain flexibility.
repository: snyk/cli
label: API
language: Go
comments_count: 2
repository_stars: 5178
---

Design interfaces that balance simplicity with extensibility. Consolidate related parameters into cohesive data structures to reduce interface complexity, while using interfaces to enable future implementations and maintain flexibility.

When designing function signatures, group related parameters into structured types rather than passing multiple individual parameters. This reduces cognitive load and makes the interface more maintainable.

For extensibility, define interfaces even when only one implementation currently exists if you anticipate future variations. This prevents breaking changes later.

Example:
```go
// Instead of multiple parameters:
func Execute(port int, certLocation string, proxyHost string, proxyPort int, args []string)

// Consolidate related data:
type ProxyInfo struct {
    Port int
    CertificateLocation string
    Host string
    ProxyPort int
}

func Execute(proxyInfo *ProxyInfo, args []string)

// Use interfaces for extensibility:
type AuthenticationHandlerInterface interface {
    Authenticate() error
}
```

This approach creates cleaner APIs that are easier to use, test, and extend over time.