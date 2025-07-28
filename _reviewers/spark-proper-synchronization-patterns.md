---
title: Proper synchronization patterns
description: When implementing synchronization mechanisms, avoid common anti-patterns
  that can lead to performance issues or incorrect behavior. Use proper condition
  variables with timeouts instead of indefinite or busy waiting, and ensure condition
  checks occur after wait operations.
repository: apache/spark
label: Concurrency
language: Other
comments_count: 3
repository_stars: 41554
---

When implementing synchronization mechanisms, avoid common anti-patterns that can lead to performance issues or incorrect behavior. Use proper condition variables with timeouts instead of indefinite or busy waiting, and ensure condition checks occur after wait operations.

Key guidelines:
1. **Use timeouts for blocking operations**: Replace indefinite waits with configurable timeouts to prevent threads from blocking forever
2. **Prefer condition variables over busy waiting**: Use `wait()/notify()` mechanisms instead of polling in loops with `Thread.sleep()`
3. **Check conditions after waiting**: Always re-evaluate the condition after a wait operation, as spurious wakeups can occur

Example of proper synchronization pattern:
```scala
private def awaitProcessThisPartition(
    id: StateStoreProviderId,
    timeoutMs: Long): Boolean = maintenanceThreadPoolLock synchronized {
  val endTime = System.currentTimeMillis() + timeoutMs
  
  var canProcessThisPartition = processThisPartition(id)
  while (!canProcessThisPartition && System.currentTimeMillis() < endTime) {
    maintenanceThreadPoolLock.wait(timeoutMs)
    canProcessThisPartition = processThisPartition(id)  // Check condition AFTER wait
  }
  
  canProcessThisPartition
}
```

This approach prevents resource waste from busy waiting, avoids indefinite blocking, and ensures correct behavior even with spurious wakeups.