---
title: Choose appropriate synchronization primitives
description: 'Select the right synchronization mechanism based on your specific use
  case to avoid performance regressions and ensure thread safety. Follow these guidelines:'
repository: argoproj/argo-cd
label: Concurrency
language: Go
comments_count: 5
repository_stars: 20149
---

Select the right synchronization mechanism based on your specific use case to avoid performance regressions and ensure thread safety. Follow these guidelines:

**Context Management**: Always call `defer cancel()` immediately after creating a cancellable context to ensure proper cleanup:
```go
ctx, cancel := context.WithCancel(c.Context())
defer cancel()
```

**Mutex Selection**: Prefer regular `sync.Mutex` over `sync.RWMutex` unless you have a read-heavy workload. RWMutex can be less efficient and cause performance regressions in typical scenarios.

**Atomic Operations**: Use modern atomic types like `atomic.Int64` instead of manual atomic operations on primitive types for better safety and readability.

**Test Synchronization**: Use channels or other explicit synchronization mechanisms in tests to avoid flakiness, rather than relying on timing:
```go
done := make(chan struct{})
go func() {
    // test logic
    close(done)
}()
<-done // wait for completion
```

**Race Condition Prevention**: In timeout scenarios with context cancellation, ensure proper ordering of operations and consider using locks when multiple goroutines access shared state concurrently.