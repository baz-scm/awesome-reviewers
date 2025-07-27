---
title: Balance concurrent operations
description: When implementing concurrent operations, carefully balance performance
  gains with resource consumption and system stability. Set conservative concurrency
  limits initially and adjust based on performance metrics rather than assuming higher
  parallelism is always better.
repository: snyk/cli
label: Concurrency
language: TypeScript
comments_count: 3
repository_stars: 5178
---

When implementing concurrent operations, carefully balance performance gains with resource consumption and system stability. Set conservative concurrency limits initially and adjust based on performance metrics rather than assuming higher parallelism is always better.

Key considerations:
- Start with lower concurrency limits (e.g., 2-5) and increase gradually after testing
- Optimize async workflows by avoiding unnecessary waiting - don't wait for all operations to complete before starting dependent tasks
- Consider whether operations should be sequential or parallel based on resource requirements and dependencies

Example of optimized async workflow:
```typescript
// Instead of waiting for all inspects to complete before processing
const results = await Promise.all(
  args.map((arg) => detectInspectMonitor(arg, options))
);

// Process incrementally to start dependent operations sooner
const snapshots: Array<Promise<Result>> = [];
for (const path of args) {
  const inspectResult = await inspect(path);
  // Start snapshot saving immediately, don't wait
  snapshots.push(saveSnapshot(inspectResult, options));
}
const results = await Promise.all(snapshots);
```

This approach reduces overall execution time while maintaining controlled resource usage and predictable behavior.