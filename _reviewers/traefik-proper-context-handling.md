---
title: proper context handling
description: Always propagate contexts consistently throughout the call chain and
  handle context cancellation properly in concurrent operations. When a context is
  available in the current scope, reuse it instead of creating a new background context.
  For operations that may block (like time.Sleep), use context-aware alternatives
  to prevent goroutine leaks when requests...
repository: traefik/traefik
label: Concurrency
language: Go
comments_count: 2
repository_stars: 55772
---

Always propagate contexts consistently throughout the call chain and handle context cancellation properly in concurrent operations. When a context is available in the current scope, reuse it instead of creating a new background context. For operations that may block (like time.Sleep), use context-aware alternatives to prevent goroutine leaks when requests are cancelled.

Example of proper context cancellation handling:
```go
// Instead of:
time.Sleep(res.Delay)

// Use:
select {
case <-ctx.Done():
    return Result{Ok: false}, nil
case <-time.After(res.Delay):
}
```

This ensures that goroutines don't remain active after their associated request context has been cancelled, preventing resource leaks and improving application responsiveness.