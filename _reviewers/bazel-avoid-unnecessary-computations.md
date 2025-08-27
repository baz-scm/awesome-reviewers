---
title: Avoid unnecessary computations
description: Before performing expensive operations, check if the work is actually
  needed or if more efficient alternatives exist. This includes validating preconditions,
  using optimized system calls, and avoiding duplicate method invocations.
repository: bazelbuild/bazel
label: Performance Optimization
language: Java
comments_count: 6
repository_stars: 24489
---

Before performing expensive operations, check if the work is actually needed or if more efficient alternatives exist. This includes validating preconditions, using optimized system calls, and avoiding duplicate method invocations.

Key patterns to apply:

1. **Guard expensive operations with feature flags**: Don't perform costly work when features are disabled. For example, avoid expensive cache pruning operations that add startup time for users not using the feature.

2. **Use efficient system calls**: Replace multiple system calls with single, more informative ones:
```java
// Instead of:
if (!path.exists()) {
  return true;
}

// Use:
var stat = path.statNullable();
if (stat == null) {
  return true;
}
```

3. **Cache method results**: Avoid calling the same method multiple times:
```java
// Instead of:
if(Profiler.getProcessCpuTimeMaybe() != null) {
  // ... use Profiler.getProcessCpuTimeMaybe() again
}

// Use:
var processCpuTime = Profiler.getProcessCpuTimeMaybe();
if(processCpuTime != null) {
  // ... use processCpuTime
}
```

4. **Check for no-op conditions**: Skip expensive operations when they won't change the result:
```java
if (pathMapper.isNoop()) {
  return new StringValue(name);
}
// ... expensive path mapping logic
```

5. **Use efficient collection operations**: Prefer built-in optimized methods over manual iteration:
```java
// Instead of manual filtering with singleton lists
// Use Iterables.filter to avoid allocation overhead
```

This approach reduces unnecessary CPU cycles, I/O operations, and memory allocations, leading to better overall performance.