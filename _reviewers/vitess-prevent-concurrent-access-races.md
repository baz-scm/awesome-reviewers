---
title: Prevent concurrent access races
description: When sharing data across goroutines, always use proper synchronization
  mechanisms to prevent race conditions. Race conditions are difficult to debug and
  can cause intermittent failures that only appear under load.
repository: vitessio/vitess
label: Concurrency
language: Go
comments_count: 8
repository_stars: 19815
---

When sharing data across goroutines, always use proper synchronization mechanisms to prevent race conditions. Race conditions are difficult to debug and can cause intermittent failures that only appear under load.

**Key practices:**

1. **Always protect mutex unlocking with defer**:
```go
func() {
    mu.Lock()
    defer mu.Unlock()
    // Code that might panic or return early
}()
```

2. **Clone data structures before sharing across goroutines**:
```go
// When parallelism > 1, clone to prevent concurrent modifications
if parallelism > 1 {
    resp = resp.CloneVT()
}
```

3. **Use atomic operations for simple flags**:
```go
var rowAdded atomic.Bool
// Later in code executed by multiple goroutines
if len(rresult.Rows) > 0 {
    rowAdded.Store(true)
}
// Check safely
if rowAdded.Load() {
    // ...
}
```

4. **Return copies of slices to prevent external mutation**:
```go
func (ml *MemoryLogger) LogEvents() []*logutilpb.Event {
    ml.mu.Lock()
    defer ml.mu.Unlock()
    return slices.Clone(ml.Events)
}
```

5. **Always clean up resources with defer**:
```go
ctx, cancel := context.WithCancel(ctx)
defer cancel() // Prevents context leaks
```

6. **Consider message queues for channels with unbounded consumers**:
```go
// For high-throughput messaging where backpressure is a concern
mq := concurrency.NewMessageQueue[*TabletHealth]()
go func() {
    for {
        th, validRes := mq.Receive()
        if validRes {
            c <- th
        }
    }
}()
```

7. **Use `chan struct{}` over `chan bool` for signaling**:
```go
// More efficient and idiomatic for simple signaling
semAcquiredChan := make(chan struct{})
// When signaling
semAcquiredChan <- struct{}{}
```

Run tests with the `-race` flag to catch race conditions during development.