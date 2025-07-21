---
title: Safe lock usage patterns
description: 'Follow these critical patterns when using locks to prevent deadlocks,
  resource leaks, and performance issues:


  1. Use consistent lock naming:

  ```go

  // Prefer'
repository: temporalio/temporal
label: Concurrency
language: Go
comments_count: 4
repository_stars: 14953
---

Follow these critical patterns when using locks to prevent deadlocks, resource leaks, and performance issues:

1. Use consistent lock naming:
```go
// Prefer
taskTrackerLock sync.RWMutex
// Over
taskTrackerMu sync.RWMutex
```

2. Never perform I/O or long-running operations while holding a lock:
```go
// Bad
func (s *Service) ProcessData() {
    s.lock.Lock()
    defer s.lock.Unlock()
    response := s.client.Call() // I/O operation!
    // ...
}

// Good
func (s *Service) ProcessData() {
    response := s.client.Call() // Do I/O first
    
    s.lock.Lock()
    defer s.lock.Unlock()
    // Only use lock for quick state updates
}
```

3. Always clean up timers properly to prevent goroutine leaks:
```go
if !timer.Stop() {
    select {
    case <-timer.C: // drain the channel if fired
    default:
    }
}
```

4. Use timeouts and context propagation to prevent indefinite lock holding:
```go
ctx, cancel := context.WithTimeout(ctx, taskTimeout)
defer cancel()

s.lock.Lock()
defer s.lock.Unlock()

select {
case <-ctx.Done():
    return ctx.Err()
case <-s.workChan:
    // Process work
}
```