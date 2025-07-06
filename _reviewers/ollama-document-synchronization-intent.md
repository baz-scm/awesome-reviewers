---
title: Document synchronization intent
description: 'Always clearly document the purpose and scope of synchronization primitives
  (mutexes, read-write locks) by:


  1. Placing them directly adjacent to the data they protect'
repository: ollama/ollama
label: Concurrency
language: Go
comments_count: 5
repository_stars: 145704
---

Always clearly document the purpose and scope of synchronization primitives (mutexes, read-write locks) by:

1. Placing them directly adjacent to the data they protect
2. Adding comments explaining what's being protected when not obvious
3. Making locking requirements explicit in method/function documentation

This practice prevents race conditions and helps future developers understand the concurrent access patterns in your code.

**Bad example:**
```go
var mu sync.Mutex
// ... many lines later or in another function ...
func doSomething() {
    mu.Lock()
    // use some shared data
    mu.Unlock()
}
```

**Good example:**
```go
// UserCache guards access to the user data map
var (
    userCache map[string]UserData
    userCacheMu sync.RWMutex  // guards userCache
)

// GetUser returns user data, safe for concurrent access
// Locking: Acquires userCacheMu read lock
func GetUser(id string) (UserData, bool) {
    userCacheMu.RLock()
    defer userCacheMu.RUnlock()
    data, found := userCache[id]
    return data, found
}
```

When synchronizing access to maps or slices, consider using a dedicated synchronized wrapper type that enforces the locking protocol rather than managing locks separately. For synchronized data structures, ensure methods that return internal state (like Maps) return copies rather than references to prevent race conditions from external modifications.