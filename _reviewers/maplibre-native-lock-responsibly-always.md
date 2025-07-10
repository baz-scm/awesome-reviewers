---
title: Lock responsibly, always
description: 'Ensure proper management of locks and concurrent resources throughout
  their lifecycle. When implementing concurrency:


  1. Encapsulate locking/unlocking in appropriate methods rather than duplicating
  code'
repository: maplibre/maplibre-native
label: Concurrency
language: Java
comments_count: 2
repository_stars: 1411
---

Ensure proper management of locks and concurrent resources throughout their lifecycle. When implementing concurrency:

1. Encapsulate locking/unlocking in appropriate methods rather than duplicating code
2. Be mindful of which threads acquire locks and consider thread-safety implications
3. Implement proper timeout handling for waiting on concurrent operations
4. Account for race conditions during cleanup of concurrent resources

**Example:**
```java
// Good: Locks encapsulated in methods where they're used
public String getResourcesCachePath() {
    resourcesCachePathLoaderLock.lock();
    try {
        // critical section operations
        return resourcesCachePath;
    } finally {
        resourcesCachePathLoaderLock.unlock();
    }
}

// For waiting on task queues, implement timeouts and handle potential race conditions
public int waitForEmpty(long timeoutMillis) {
    // Implementation that respects timeout and returns remaining tasks
    // without resetting timeout if new tasks are added
}
```

Avoid duplicating locking code across methods, and ensure locks are released in finally blocks to prevent deadlocks. When implementing methods that wait for concurrent operations to complete, provide sensible timeout options and consider the implications of race conditions.