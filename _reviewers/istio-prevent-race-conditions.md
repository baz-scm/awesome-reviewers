---
title: prevent race conditions
description: 'Always protect shared state access and ensure proper synchronization
  in concurrent operations to prevent race conditions. Key areas to review:


  1. **Shared Data Mutation**: Never mutate shared data structures without proper
  synchronization. If data is accessed by multiple goroutines, use locks or create
  copies instead of in-place mutations.'
repository: istio/istio
label: Concurrency
language: Go
comments_count: 6
repository_stars: 37192
---

Always protect shared state access and ensure proper synchronization in concurrent operations to prevent race conditions. Key areas to review:

1. **Shared Data Mutation**: Never mutate shared data structures without proper synchronization. If data is accessed by multiple goroutines, use locks or create copies instead of in-place mutations.

```go
// Bad: Mutating shared slice in-place
func (ep *IstioEndpoint) SortAddresses() []string {
    sort.Sort(sort.Reverse(sort.StringSlice(ep.Addresses))) // Race condition!
    return ep.Addresses
}

// Good: Create copy or use proper locking
func (ep *IstioEndpoint) SortAddresses() []string {
    ep.mu.Lock()
    defer ep.mu.Unlock()
    addrSlice := make([]string, len(ep.Addresses))
    copy(addrSlice, ep.Addresses)
    sort.Sort(sort.Reverse(sort.StringSlice(addrSlice)))
    return addrSlice
}
```

2. **Event Processing Order**: When multiple informers or event handlers process the same resources, ensure proper ordering or make handlers idempotent to handle events arriving in any order.

3. **Context Cancellation**: Always respect context cancellation in long-running operations, especially during sleep or wait periods:

```go
// Bad: Sleep blocks context cancellation
time.Sleep(next)

// Good: Respect context during sleep
select {
case <-time.After(next):
case <-ctx.Done():
    return ctx.Err()
}
```

4. **Lock Ordering**: When acquiring multiple locks or waiting for synchronization, establish clear ordering to prevent deadlocks. Consider whether locks should be acquired before or after waiting for external conditions.

5. **Test Flakiness**: If tests are flaky due to timing issues, make them more robust by allowing for multiple valid event sequences rather than expecting exact ordering, especially in distributed systems where event coalescing can occur.