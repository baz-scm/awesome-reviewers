---
title: Use proper synchronization primitives
description: When implementing concurrent operations, always use appropriate synchronization
  mechanisms and ensure all asynchronous code paths complete properly. This includes
  specifying explicit timing parameters, using efficient blocking primitives, and
  guaranteeing promise resolution in all execution branches.
repository: nrwl/nx
label: Concurrency
language: TypeScript
comments_count: 3
repository_stars: 27518
---

When implementing concurrent operations, always use appropriate synchronization mechanisms and ensure all asynchronous code paths complete properly. This includes specifying explicit timing parameters, using efficient blocking primitives, and guaranteeing promise resolution in all execution branches.

Key practices:
1. **Explicit timing**: Always specify delay values in timing functions like setTimeout() with clear documentation of the reasoning
2. **Efficient synchronization**: Use proper blocking primitives like Atomics.wait() instead of busy polling when waiting for other processes
3. **Complete async paths**: Ensure all code branches in asynchronous operations properly resolve or reject promises

Example of proper synchronization:
```typescript
// Bad: Missing delay parameter
setTimeout(() => {
  this.sendToDaemonViaQueue(msg).then(res, rej);
});

// Good: Explicit delay with reasoning
setTimeout(() => {
  // Wait 100ms for daemon to finish shutting down
  this.sendToDaemonViaQueue(msg).then(res, rej);
}, 100);

// Good: Efficient blocking with Atomics.wait
while (!projectGraphCache && Date.now() - startTime < maxWaitTime) {
  Atomics.wait(sharedArray, 0, 0, pollInterval);
  projectGraphCache = readProjectGraphCache(minimumComputedAt);
}

// Good: Promise resolved in all paths
this.childProcess.onExit((message) => {
  this.isAlive = false;
  const code = messageToCode(message);
  this.childProcess.cleanup();
  this.exitCallbacks.forEach((cb) => cb(code));
  res({ success: false, code, terminalOutput: this.terminalOutput }); // Don't forget this!
});
```

This prevents race conditions, ensures predictable timing behavior, and maintains proper async operation completion.