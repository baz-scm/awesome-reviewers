---
title: Thread-safe shared state
description: Ensure that shared mutable state is properly protected against concurrent
  access to prevent race conditions and data corruption. When multiple threads can
  access the same mutable data, use appropriate synchronization mechanisms such as
  ThreadLocal, locks, or atomic operations.
repository: facebook/react-native
label: Concurrency
language: Java
comments_count: 10
repository_stars: 123178
---

Ensure that shared mutable state is properly protected against concurrent access to prevent race conditions and data corruption. When multiple threads can access the same mutable data, use appropriate synchronization mechanisms such as ThreadLocal, locks, or atomic operations.

Key indicators that thread safety is needed:
- Static mutable fields accessed by multiple threads
- Shared objects modified during overlapping operations
- State that assumes single-threaded access but may be accessed concurrently

Common solutions:
- Use ThreadLocal for thread-specific instances of shared data
- Implement proper state tracking for overlapping operations
- Add null checks and validation for data that may be modified concurrently

Example transformation from unsafe to thread-safe code:

```java
// UNSAFE: Static arrays shared across threads
private static final Object[] VIEW_MGR_ARGS = new Object[2];

// SAFE: ThreadLocal ensures each thread has its own instance
private static final ThreadLocal<Object[]> VIEW_MGR_ARGS =
    new ThreadLocal<Object[]>() {
        @Override
        protected Object[] initialValue() {
            return new Object[2];
        }
    };
```

For overlapping operations, maintain proper state tracking:

```java
// Track multiple concurrent operations instead of single boolean flag
private Set<Integer> transitioningChildren = new HashSet<>();

public void startViewTransition(View view) {
    transitioningChildren.add(view.getId());
}

public void endViewTransition(View view) {
    transitioningChildren.remove(view.getId());
    // Only clear state when no more transitions are active
    if (transitioningChildren.isEmpty()) {
        clearTransitionState();
    }
}
```

Always consider the timing and ordering of operations that modify shared state, and add appropriate null checks for data that may be modified by concurrent operations.