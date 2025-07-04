---
title: Optimize algorithmic operations
description: 'Before implementing or modifying algorithms, carefully evaluate data
  structure properties and operation costs. Always:


  1. **Understand data structure guarantees**: Choose structures that provide the
  necessary ordering and performance characteristics. For instance, when replacing
  one structure with another, be aware of their different behaviors:'
repository: quarkusio/quarkus
label: Algorithms
language: Java
comments_count: 5
repository_stars: 14667
---

Before implementing or modifying algorithms, carefully evaluate data structure properties and operation costs. Always:

1. **Understand data structure guarantees**: Choose structures that provide the necessary ordering and performance characteristics. For instance, when replacing one structure with another, be aware of their different behaviors:

```java
// Problematic: PriorityBlockingQueue doesn't guarantee ordering for equal priorities
private final PriorityBlockingQueue<ShutdownTask> shutdownTasks = new PriorityBlockingQueue<>();

// Better: If order matters for equal priorities, use a secondary comparison key
private final PriorityBlockingQueue<ShutdownTask> shutdownTasks = 
    new PriorityBlockingQueue<>(11, Comparator
        .comparing(ShutdownTask::getPriority)
        .thenComparing(ShutdownTask::getCreationOrder));
```

2. **Avoid unnecessary computations**: Eliminate redundant operations by:
   - Deriving one data structure from another when they contain inverse or related data
   - Leveraging existing ordering instead of re-sorting collections
   - Using the most efficient implementation for your specific case (e.g., specific `List.of()` implementations)

3. **Choose appropriate algorithms**: Select the right algorithm for specific operations like version comparison, ensuring it handles edge cases correctly:

```java
// Better performance and correctness for version comparisons
new ComparableVersion("2.10.0.CR1").compareTo(new ComparableVersion(version))
```

These optimizations improve both performance and correctness of your code while keeping it maintainable.