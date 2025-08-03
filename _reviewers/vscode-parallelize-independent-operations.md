---
title: Parallelize independent operations
description: When writing concurrent code, always execute independent operations in
  parallel rather than sequentially to improve performance and responsiveness. Using
  parallel execution patterns can significantly reduce waiting time for I/O-bound
  operations.
repository: microsoft/vscode
label: Concurrency
language: TypeScript
comments_count: 3
repository_stars: 174887
---

When writing concurrent code, always execute independent operations in parallel rather than sequentially to improve performance and responsiveness. Using parallel execution patterns can significantly reduce waiting time for I/O-bound operations.

For API calls or file operations that don't depend on each other:

```typescript
// Instead of sequential execution:
const entitlements = await this.getEntitlements(session.accessToken, tokenEntitlementUrl);
const chatEntitlements = await this.getChatEntitlements(session.accessToken, chatEntitlementUrl);

// Prefer parallel execution:
const [entitlements, chatEntitlements] = await Promise.all([
  this.getEntitlements(session.accessToken, tokenEntitlementUrl),
  this.getChatEntitlements(session.accessToken, chatEntitlementUrl)
]);
```

When implementing operations that can take variable time to complete:
1. Consider using `Promise.race()` to process results as they arrive
2. Always respect cancellation tokens in long-running operations
3. Include proper cleanup mechanisms after parallel execution

Remember that excessive parallelism can lead to resource contention, so balance parallelism with the available system resources. For CPU-bound tasks, consider using worker threads or a task queue to prevent blocking the main thread.