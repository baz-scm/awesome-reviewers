---
title: Deterministic lock management
description: Always ensure locks are acquired and released in a deterministic manner
  in concurrent code. Use `defer` statements immediately after lock acquisition to
  guarantee release along all code paths, and acquire locks before accessing the protected
  resources to prevent race conditions.
repository: oven-sh/bun
label: Concurrency
language: Other
comments_count: 3
repository_stars: 79093
---

Always ensure locks are acquired and released in a deterministic manner in concurrent code. Use `defer` statements immediately after lock acquisition to guarantee release along all code paths, and acquire locks before accessing the protected resources to prevent race conditions.

Example of proper lock usage:
```zig
pub fn someOperation(self: *SomeStruct) void {
    self.mutex.lock();
    defer self.mutex.unlock();
    
    // If reference counting is involved, also defer the deref
    defer self.deref();
    
    // Access protected resources safely here...
    // All code paths will automatically release the lock
}
```

Incorrect pattern that can lead to race conditions:
```zig
// AVOID: Accessing protected data before acquiring the lock
var item = self.shared_map.get(key); // Race condition!
self.lock.lock();
// ... operations with item ...
self.lock.unlock();
```

Correct approach:
```zig
// CORRECT: Acquire lock first, then access protected data
self.lock.lock();
defer self.lock.unlock();
var item = self.shared_map.get(key); // Safe access
// ... operations with item ...
```

This pattern eliminates duplicate unlock calls along different code paths, prevents deadlocks, and ensures thread safety when accessing shared resources.