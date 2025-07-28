---
title: Prevent async race conditions
description: Identify and prevent race conditions in asynchronous operations, especially
  when operations depend on each other's completion state. Race conditions occur when
  the timing or order of async operations affects program correctness, often leading
  to intermittent failures that are difficult to debug.
repository: cline/cline
label: Concurrency
language: TypeScript
comments_count: 3
repository_stars: 48299
---

Identify and prevent race conditions in asynchronous operations, especially when operations depend on each other's completion state. Race conditions occur when the timing or order of async operations affects program correctness, often leading to intermittent failures that are difficult to debug.

Common scenarios include:
- UI operations that depend on view state (focus, visibility)
- Authentication flows with shared state
- Operations that assume previous async work has completed

Instead of using arbitrary timeouts, use proper synchronization mechanisms like condition waiting, promises, or explicit state checking.

Example from the codebase:
```typescript
// Problem: Race condition - command returns before UI is ready
await vscode.commands.executeCommand("cline.focusChatInput")
// This executes too early, before focus is actually set
visibleWebview?.controller.fixWithCline(...)

// Better: Use proper waiting mechanism
await vscode.commands.executeCommand("cline.focusChatInput")
await pWaitFor(() => webviewIsFocused()) // Wait for actual condition
visibleWebview?.controller.fixWithCline(...)
```

Always consider: What assumptions am I making about timing? Could this operation execute before its dependencies are ready? What happens if this code runs concurrently with itself?