---
title: Safe concurrent programming
description: 'When working with concurrent code, carefully manage shared resources
  and synchronization to prevent race conditions, deadlocks, and resource leaks:


  1. **Protect shared data**: Always synchronize access to data accessed by multiple
  goroutines using appropriate primitives like mutexes or channels.'
repository: grafana/grafana
label: Concurrency
language: Go
comments_count: 7
repository_stars: 68825
---

When working with concurrent code, carefully manage shared resources and synchronization to prevent race conditions, deadlocks, and resource leaks:

1. **Protect shared data**: Always synchronize access to data accessed by multiple goroutines using appropriate primitives like mutexes or channels.

```go
// BAD: Accessing map from multiple goroutines without synchronization
go func() {
    runErrs[testServer.id] = err  // Race condition!
}()

// GOOD: Use mutex to protect shared map
var mu sync.Mutex
go func() {
    mu.Lock()
    defer mu.Unlock()
    runErrs[testServer.id] = err
}()
```

2. **Deep copy shared objects**: When passing data to goroutines, make defensive copies to prevent concurrent modification.

```go
// BAD: Modifying the same object across goroutines
go func() {
    // Both goroutines modify the same object
    created.Status = "processing" 
}()

// GOOD: Create a copy for the goroutine to modify
go func() {
    createdCopy := created.DeepCopyObject()
    createdCopy.Status = "processing"
}()
```

3. **Resource cleanup**: Use `defer` to ensure resources are always cleaned up, even in error paths.

```go
// BAD: Channel might not be closed on some error paths
if err != nil {
    return  // events channel never closed!
}
close(events)

// GOOD: Guarantee cleanup with defer
defer close(events)
```

4. **Context propagation**: Properly handle context cancellation in goroutines to allow graceful shutdown.

```go
// BAD: Using Background context disconnects from parent cancellation
go func() {
    ctx := context.Background()  // Ignores parent cancellation signals
    // long-running operation that won't be cancelled
}()

// GOOD: Propagate the original context
go func() {
    // This operation will be cancelled when parent context is cancelled
    select {
    case <-ctx.Done():
        return
    case <-time.After(5 * time.Second):
        // continue processing
    }
}()
```

5. **Channel communication**: Be aware of ordering and blocking issues when sending from multiple goroutines to a single channel.

```go
// BAD: Multiple goroutines racing to send to channel can cause ordering issues
go func() {
    stream <- event  // May race with other senders
}()

// GOOD: Use a central goroutine to manage channel sends
eventQueue := make(chan Event, 100)
go func() {
    for event := range eventQueue {
        stream <- event  // Maintains ordering
    }
}()
```

6. **Signaling completion**: Use channel close for signaling instead of sending values.

```go
// BAD: Sending value for signaling
st.stateRunnerShutdown <- struct{}{}

// GOOD: Closing channel for signaling
close(st.stateRunnerShutdown)
```