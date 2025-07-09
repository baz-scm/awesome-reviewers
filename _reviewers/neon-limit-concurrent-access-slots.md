---
title: Limit concurrent access slots
description: Design concurrency mechanisms based on actual usage patterns rather than
  theoretical maximum connections. When implementing locking or state tracking for
  concurrent operations, limit the number of concurrent slots to a reasonable value
  (e.g., 128) that reflects the expected concurrency level, rather than scaling to
  the maximum number of possible backends...
repository: neondatabase/neon
label: Concurrency
language: Other
comments_count: 2
repository_stars: 19015
---

Design concurrency mechanisms based on actual usage patterns rather than theoretical maximum connections. When implementing locking or state tracking for concurrent operations, limit the number of concurrent slots to a reasonable value (e.g., 128) that reflects the expected concurrency level, rather than scaling to the maximum number of possible backends (max_connections). This approach reduces memory overhead and lock contention.

For example, instead of:
```c
// Creating state tracking for every possible backend
prewarm_worker_state[MaxConnections];
```

Use a more efficient approach:
```c
// Limit concurrent slots to what's actually needed
#define MAX_CONCURRENT_PREWARMING 128
prewarm_worker_state[MAX_CONCURRENT_PREWARMING];
```

This is especially effective when the operation is quick (as with prewarming or prefetching), making it unlikely that all backends would need concurrent access. The same principle applies to other synchronization mechanisms like locks, semaphores, or condition variables.