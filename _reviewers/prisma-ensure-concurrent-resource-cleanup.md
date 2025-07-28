---
title: Ensure concurrent resource cleanup
description: Always ensure proper cleanup of concurrent resources like semaphores,
  transactions, and async operations, even when exceptions occur. Use finally blocks
  to guarantee resource release and Promise.allSettled instead of Promise.all when
  handling multiple concurrent operations that might fail.
repository: prisma/prisma
label: Concurrency
language: TypeScript
comments_count: 4
repository_stars: 42967
---

Always ensure proper cleanup of concurrent resources like semaphores, transactions, and async operations, even when exceptions occur. Use finally blocks to guarantee resource release and Promise.allSettled instead of Promise.all when handling multiple concurrent operations that might fail.

Key patterns to follow:
- Wrap resource acquisition/release in try-finally blocks to prevent resource leaks
- Use Promise.allSettled for concurrent operations where some failures are acceptable
- Implement timeouts for operations that might hang indefinitely
- Consider using AbortController for proper termination of long-running concurrent operations

Example:
```typescript
// Good: Guaranteed cleanup with finally
const semaphore = new Semaphore(maxWorkers)
await semaphore.acquire()
const pendingJob = (async () => {
  try {
    // do work
  } finally {
    semaphore.release() // Always released, even on exception
  }
})()

// Good: Handle failures gracefully in concurrent operations  
await Promise.allSettled([...transactions.values()].map(tx => closeTransaction(tx)))

// Good: Prevent hanging with timeout
const timeout = setTimeout(() => resolve(''), 1000)
```

This prevents deadlocks, resource exhaustion, and hanging operations that can severely impact application reliability in concurrent scenarios.