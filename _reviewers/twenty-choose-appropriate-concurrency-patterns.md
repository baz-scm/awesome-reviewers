---
title: Choose appropriate concurrency patterns
description: Select concurrency mechanisms that align with your system architecture
  and established codebase patterns. Avoid using database transactions and pessimistic
  locking when working with connection pooling, as they can cause unintended side
  effects where one connection commits on behalf of another. Instead, follow existing
  patterns in the codebase for handling...
repository: twentyhq/twenty
label: Concurrency
language: TypeScript
comments_count: 3
repository_stars: 35477
---

Select concurrency mechanisms that align with your system architecture and established codebase patterns. Avoid using database transactions and pessimistic locking when working with connection pooling, as they can cause unintended side effects where one connection commits on behalf of another. Instead, follow existing patterns in the codebase for handling race conditions and ensuring data consistency.

For workload distribution, prefer job-based parallelization over sequential processing. Rather than iterating through all workspaces in a single job, enqueue separate jobs for each workspace to enable parallel processing and better resource utilization.

When designing async operations, consider the proper sequencing of dependent tasks. For example, synchronization operations should be ordered appropriately - sync folders before processing messages to detect user changes.

Example of preferred job distribution pattern:
```typescript
// Instead of processing all workspaces sequentially:
for (const activeWorkspace of activeWorkspaces) {
  await processWorkspace(activeWorkspace);
}

// Enqueue separate jobs for parallel processing:
for (const activeWorkspace of activeWorkspaces) {
  await this.messageQueue.add('process-workspace', { 
    workspaceId: activeWorkspace.id 
  });
}
```

This approach improves system performance, reduces blocking operations, and follows established concurrency patterns that work well with the existing infrastructure.