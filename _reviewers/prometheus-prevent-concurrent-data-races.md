---
title: prevent concurrent data races
description: Always analyze shared data access patterns to prevent race conditions
  in concurrent code. Use appropriate synchronization mechanisms based on access patterns
  and data ownership.
repository: prometheus/prometheus
label: Concurrency
language: Go
comments_count: 4
repository_stars: 59616
---

Always analyze shared data access patterns to prevent race conditions in concurrent code. Use appropriate synchronization mechanisms based on access patterns and data ownership.

Key practices:
1. **Use RLock for read-heavy scenarios**: When data is read frequently but written rarely, use `sync.RWMutex` with `RLock()` to allow concurrent reads while still protecting against concurrent writes.

2. **Copy data when sharing between goroutines**: When the same data structure will be accessed by multiple goroutines that might modify it, create copies to prevent races.

3. **Avoid unmanaged goroutines**: Don't spawn goroutines without proper lifecycle management. Use `sync.WaitGroup` or context cancellation to ensure cleanup.

4. **Understand library thread safety**: Before adding locks around external library calls, verify if the library is already thread-safe. Adding unnecessary locks can cause performance issues.

Example of proper data copying to prevent races:
```go
func relabelAlerts(alerts []*Alert) []*Alert {
    var relabeledAlerts []*Alert
    for _, s := range alerts {
        // Copy the alert to avoid race condition when multiple 
        // goroutines modify the same alert pointers
        a := s.Copy()
        // ... relabel operations on copy
        relabeledAlerts = append(relabeledAlerts, a)
    }
    return relabeledAlerts
}
```

Always run tests with `-race` flag to detect potential race conditions during development.