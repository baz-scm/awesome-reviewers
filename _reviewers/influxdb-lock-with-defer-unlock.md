---
title: Lock with defer unlock
description: Always follow the lock-defer-unlock pattern when protecting shared resources
  with mutexes. Acquire the lock, immediately use defer to ensure unlock, then perform
  operations on the protected resource. This prevents deadlocks and ensures locks
  are released even when functions exit unexpectedly.
repository: influxdata/influxdb
label: Concurrency
language: Go
comments_count: 8
repository_stars: 30268
---

Always follow the lock-defer-unlock pattern when protecting shared resources with mutexes. Acquire the lock, immediately use defer to ensure unlock, then perform operations on the protected resource. This prevents deadlocks and ensures locks are released even when functions exit unexpectedly.

When returning data from mutex-protected resources, always create a deep copy before returning to prevent race conditions after the lock is released.

```go
// Bad
func (s *Store) ClearBadShardList() map[uint64]error {
    s.badShards.mu.Lock()
    // Missing defer - risk of not unlocking if code between lock and unlock panics
    if s.badShards.shardErrors == nil {
        s.badShards.shardErrors = make(map[uint64]error)
    }
    badShards := maps.Clone(s.badShards.shardErrors)
    clear(s.badShards.shardErrors)
    s.badShards.mu.Unlock()
    
    return badShards
}

// Good
func (s *Store) ClearBadShardList() map[uint64]error {
    s.badShards.mu.Lock()
    defer s.badShards.mu.Unlock()
    
    if s.badShards.shardErrors == nil {
        s.badShards.shardErrors = make(map[uint64]error)
    }
    // Clone before returning to prevent race conditions
    badShards := maps.Clone(s.badShards.shardErrors)
    clear(s.badShards.shardErrors)
    
    return badShards
}
```

For read-only operations, consider using RWMutex with RLock() to allow concurrent reads. This approach increases concurrency while maintaining thread safety.