---
title: Memory ordering needs barriers
description: 'Ensure proper memory ordering in concurrent code by using appropriate
  memory barriers and atomic operations based on the access pattern. When implementing
  release-store semantics, place the store fence before the actual store to prevent
  instruction reordering:'
repository: netty/netty
label: Concurrency
language: Java
comments_count: 6
repository_stars: 34227
---

Ensure proper memory ordering in concurrent code by using appropriate memory barriers and atomic operations based on the access pattern. When implementing release-store semantics, place the store fence before the actual store to prevent instruction reordering:

```java
// INCORRECT - barrier after store
value.store(newValue);
storeFence();  // Too late!

// CORRECT - barrier before store
storeFence();  // Prevents reordering of previous stores
value.store(newValue);
```

Key guidelines:
- Use volatile for single-writer scenarios requiring visibility
- For performance-critical paths with single-threaded access, prefer lazySet() over volatile writes
- When implementing custom concurrent data structures, consider using unpadded variants for better memory efficiency
- Place state updates before notification in producer-consumer patterns to ensure proper visibility

This approach prevents subtle race conditions while maintaining performance in concurrent systems.