---
title: proper synchronization practices
description: Ensure thread safety by using appropriate synchronization mechanisms
  and understanding thread context. When working with shared mutable state, protect
  critical sections with proper synchronization to prevent race conditions and concurrent
  modifications. Choose the right synchronization approach for your use case - prefer
  language-provided utilities over...
repository: facebook/react-native
label: Concurrency
language: Kotlin
comments_count: 4
repository_stars: 123178
---

Ensure thread safety by using appropriate synchronization mechanisms and understanding thread context. When working with shared mutable state, protect critical sections with proper synchronization to prevent race conditions and concurrent modifications. Choose the right synchronization approach for your use case - prefer language-provided utilities over manual implementations when possible.

Key practices:
1. Use synchronized blocks or methods to protect shared collections from concurrent modification
2. Leverage language features like Kotlin's `lazy` delegation for thread-safe initialization instead of manual double-checked locking
3. Understand your execution context - avoid unnecessary thread switching when already on the correct thread

Example of proper synchronization:
```kotlin
// Instead of risking ConcurrentModificationException
val snapshot = ArrayList(beforeUIBlocks)
beforeUIBlocks.clear()

// Use proper synchronization
val blocksToExecute: List<UIBlock> = synchronized(this) {
    if (beforeUIBlocks.isEmpty()) return
    beforeUIBlocks.toList().also { beforeUIBlocks.clear() }
}

// Prefer lazy delegation over manual double-checked locking
private val mainHandler: Handler by lazy {
    Handler(Looper.getMainLooper())
}
```

This approach prevents race conditions, reduces complexity, and makes concurrent code more maintainable and less error-prone.