---
title: Document mutex usage
description: Always document mutex fields and their purpose, ensure proper locking/unlocking
  patterns, and avoid redundant locks when underlying structures are already thread-safe.
  When using mutexes, clearly indicate what data they protect and why the synchronization
  is necessary.
repository: gofiber/fiber
label: Concurrency
language: Go
comments_count: 4
repository_stars: 37560
---

Always document mutex fields and their purpose, ensure proper locking/unlocking patterns, and avoid redundant locks when underlying structures are already thread-safe. When using mutexes, clearly indicate what data they protect and why the synchronization is necessary.

Add comments for mutex fields explaining their purpose:
```go
// sendfilesMutex protects concurrent access to sendfiles slice
sendfilesMutex sync.RWMutex
```

Avoid redundant locking when underlying structures already provide thread safety:
```go
// The mu mutex in the Middleware struct might be redundant for operations 
// on the Session since Session struct itself already ensures thread-safety
```

Use proper defer patterns to prevent race conditions, even if slightly slower:
```go
mutex.Lock()
defer mutex.Unlock() // Prevents race conditions on shared data access
return c.Status(fiber.StatusOK).JSON(data)
```

Consider performance implications when choosing between `sync.Map` and regular maps with `RWMutex`, but prioritize correctness and clarity over micro-optimizations.