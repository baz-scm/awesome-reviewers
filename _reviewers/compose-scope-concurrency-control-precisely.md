---
title: Scope concurrency control precisely
description: Apply concurrency control mechanisms with precise scope to prevent both
  race conditions and unnecessary blocking. Use appropriate synchronization tools
  (mutex, channels, errgroup) only around critical sections that actually require
  protection.
repository: docker/compose
label: Concurrency
language: Go
comments_count: 5
repository_stars: 35858
---

Apply concurrency control mechanisms with precise scope to prevent both race conditions and unnecessary blocking. Use appropriate synchronization tools (mutex, channels, errgroup) only around critical sections that actually require protection.

Common patterns to follow:
1. Protect shared state with minimal lock scope:
```go
// Good - minimal mutex scope
mux.Lock()
// Only protect the shared state modification
project.UpdateConfig()
mux.Unlock()

// Bad - overly broad mutex scope
mux.Lock()
defer mux.Unlock()
// Blocking concurrent operations unnecessarily
runProviders()
```

2. Use errgroup for concurrent error handling:
```go
eg := errgroup.Group{}
for _, container := range containers {
    container := container // Capture loop variable
    eg.Go(func() error {
        return processContainer(ctx, container)
    })
}
return eg.Wait()
```

3. Guard against race conditions in shared data structures:
```go
// Bad - race condition on map
opts := map[string]Options{}
for _, svc := range services {
    go func() { opts[svc.Name] = buildOptions() }()
}

// Good - protected access
var mu sync.Mutex
for _, svc := range services {
    svc := svc
    go func() {
        mu.Lock()
        opts[svc.Name] = buildOptions()
        mu.Unlock()
    }()
}
```