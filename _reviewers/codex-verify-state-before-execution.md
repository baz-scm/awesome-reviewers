---
title: Verify state before execution
description: When scheduling asynchronous operations in concurrent environments, always
  verify the system state hasn't changed before executing critical operations to prevent
  race conditions. This is especially important in interactive applications where
  user actions (like cancellations) might occur between the time an operation is scheduled
  and when it executes.
repository: openai/codex
label: Concurrency
language: TypeScript
comments_count: 2
repository_stars: 31275
---

When scheduling asynchronous operations in concurrent environments, always verify the system state hasn't changed before executing critical operations to prevent race conditions. This is especially important in interactive applications where user actions (like cancellations) might occur between the time an operation is scheduled and when it executes.

To implement this pattern:
- Use appropriate timing mechanisms (setTimeout, queueMicrotask) based on requirements
- Always double-check cancellation flags and system state immediately before performing operations
- Consider using nested timing approaches for different aspects of the operation when needed

Example:
```typescript
// Instead of this:
setTimeout(() => {
  this.onItem(item);
  staged[idx] = undefined;
}, delay);

// Do this:
setTimeout(() => {
  // Double-check cancellation state right before executing
  if (
    thisGeneration === this.generation &&
    !this.canceled &&
    !this.hardAbort.signal.aborted
  ) {
    this.onItem(item);
    staged[idx] = undefined;
  }
}, delay);
```

This pattern helps maintain consistency between internal state and UI, prevents "ghost" operations from occurring after cancellation, and makes your concurrent code more robust against race conditions.