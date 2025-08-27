---
title: Executor service lifecycle
description: 'Properly manage executor service lifecycle to prevent resource leaks,
  deadlocks, and orphaned threads that can cause system inconsistencies.


  Key practices:'
repository: bazelbuild/bazel
label: Concurrency
language: Java
comments_count: 7
repository_stars: 24489
---

Properly manage executor service lifecycle to prevent resource leaks, deadlocks, and orphaned threads that can cause system inconsistencies.

Key practices:
1. **Use try-with-resources**: Always manage executors within try-with-resources blocks to ensure proper shutdown
2. **Avoid manual future cancellation**: Prefer structured concurrency patterns like `invokeAny()` over low-level `submit().get()` with manual cancellation
3. **Prevent orphaned threads**: Ensure worker threads are properly joined before allowing new operations to proceed
4. **Choose appropriate synchronization**: Use higher-level primitives like `Phaser` instead of combining multiple lower-level mechanisms

Example of proper executor management:
```java
try (var executor = Executors.newSingleThreadExecutor(threadFactory)) {
  // Submit tasks and get results within the try block
  var future = executor.submit(callable);
  return future.get(timeout, TimeUnit.SECONDS);
} // Executor automatically shuts down here
```

For cancellation scenarios, prefer structured approaches:
```java
// Instead of manual future cancellation
var future = executor.submit(task);
future.cancel(true);

// Use invokeAny for timeout/cancellation semantics
return executor.invokeAny(List.of(task), timeout, TimeUnit.SECONDS);
```

This prevents common issues like deadlocks when futures are never scheduled, ensures proper resource cleanup, and avoids race conditions from orphaned threads modifying shared state after new operations have begun.