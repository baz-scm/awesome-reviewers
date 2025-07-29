---
title: API interface simplification
description: Design APIs with clean, minimal interfaces that encapsulate internal
  logic and avoid exposing unnecessary complexity to consumers. Prefer methods that
  internally handle implementation details over exposing flags or parameters that
  clients must manage.
repository: traefik/traefik
label: API
language: Go
comments_count: 4
repository_stars: 55772
---

Design APIs with clean, minimal interfaces that encapsulate internal logic and avoid exposing unnecessary complexity to consumers. Prefer methods that internally handle implementation details over exposing flags or parameters that clients must manage.

Key principles:
- Encapsulate internal logic rather than exposing implementation details through exported functions or flags
- Remove unnecessary parameters when they serve no functional purpose (e.g., always-constant values)
- Maintain consistency across similar API components by extracting common functionality
- Ensure proper interface compliance when implementing required methods

Example of good encapsulation:
```go
// Instead of exposing internal state checking
if !p.k8sClient.IngressClassesIgnored() {
    ingressClasses = p.k8sClient.GetIngressClasses()
}

// Prefer encapsulated methods that handle logic internally
ingressClasses := p.k8sClient.ListIngressClasses() // internally checks ignored state
```

Example of parameter simplification:
```go
// Instead of passing unnecessary constant parameters
func AllowTokenBucketN(key string, limit, burst, ttl, t, n int) // n is always 1

// Simplify to essential parameters only
func Allow(key string, limit, burst, ttl, t int)
```

This approach reduces cognitive load on API consumers, prevents misuse of internal implementation details, and creates more maintainable interfaces that are easier to evolve over time.