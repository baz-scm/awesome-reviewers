---
title: avoid unnecessary object creation
description: Minimize object allocation in performance-critical code paths by reusing
  existing objects, caching expensive operations, and choosing efficient alternatives
  to object creation patterns.
repository: apache/kafka
label: Performance Optimization
language: Java
comments_count: 6
repository_stars: 30575
---

Minimize object allocation in performance-critical code paths by reusing existing objects, caching expensive operations, and choosing efficient alternatives to object creation patterns.

Key strategies include:

1. **Reuse existing objects instead of creating new ones**: When possible, duplicate or reuse existing objects rather than instantiating new ones. For example, use `partition.duplicate()` instead of creating a new `AlterShareGroupOffsetsResponsePartition`.

2. **Avoid Optional creation in hotspots**: In performance-critical paths, use direct null checks instead of `Optional.ofNullable()`. Replace:
```java
Optional.ofNullable(image.cluster().broker(brokerId)).ifPresent(b -> {
    // process broker
});
```
With:
```java
var broker = image.cluster().broker(brokerId);
if (broker != null && !broker.fenced() && broker.listeners().containsKey(listenerName.value())) {
    res.add(brokerId);
}
```

3. **Cache expensive operations outside loops**: When performing expensive operations like `Errors.forException()` that scan lists, compute the result once and reuse it rather than calling it repeatedly in loops.

4. **Choose efficient collection operations**: Use `Collections.unmodifiableSet()` instead of `Set.copyOf()` to avoid deep copying, and prefer direct collection operations over creating intermediate temporary collections.

5. **Optimize conditional checks**: Order conditional checks to perform cheaper operations first, such as checking `partitionInfo.leader() == null` before creating a `TopicPartition` object.

This approach is particularly important in frequently executed code paths, request processing hotspots, and tight loops where object allocation overhead can significantly impact performance.