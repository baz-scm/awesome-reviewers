---
title: Synchronization primitive selection
description: Choose appropriate synchronization primitives and ensure proper protection
  of shared state to avoid race conditions and deadlocks. Prefer regular mutexes over
  RWMutex unless read-heavy workloads justify the complexity, as RWMutex can be a
  performance trap. When accessing shared state, ensure the entire read-modify-write
  operation is atomic by keeping it...
repository: gravitational/teleport
label: Concurrency
language: Go
comments_count: 4
repository_stars: 19109
---

Choose appropriate synchronization primitives and ensure proper protection of shared state to avoid race conditions and deadlocks. Prefer regular mutexes over RWMutex unless read-heavy workloads justify the complexity, as RWMutex can be a performance trap. When accessing shared state, ensure the entire read-modify-write operation is atomic by keeping it within the same lock scope.

For goroutine coordination, consider using channels instead of mutexes when possible to avoid deadlock scenarios. When using sync.WaitGroup, understand the reuse patterns - you can reuse the same WaitGroup with Add/Wait/Done cycles, but ensure proper synchronization during the transition between tasks.

Example of proper shared state protection:
```go
// Bad - race condition between check and use
s.mu.Lock()
alreadySent := s.closeSent
s.mu.Unlock()

if !alreadySent {
    // closeSent could have changed here
    s.sendCloseMessage()
}

// Good - atomic check and action
s.mu.Lock()
if !s.closeSent {
    s.closeSent = true
    s.sendCloseMessage()
}
s.mu.Unlock()
```

Avoid holding locks during blocking operations like network I/O. Instead, use dedicated goroutines with channels for coordination:
```go
// Bad - lock held during read blocks all writes
s.websocket.Lock()
msgType, data, err := s.ws.ReadMessage()
s.websocket.Unlock()

// Good - separate goroutines with channel communication
go s.writeLoop() // handles all writes via channel
s.readLoop()     // reads without blocking writes
```