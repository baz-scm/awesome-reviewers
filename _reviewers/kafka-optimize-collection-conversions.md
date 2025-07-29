---
title: Optimize collection conversions
description: When converting between Java and Scala collections or performing set
  operations, choose methods that minimize temporary collection creation to improve
  performance and reduce memory overhead.
repository: apache/kafka
label: Algorithms
language: Other
comments_count: 4
repository_stars: 30575
---

When converting between Java and Scala collections or performing set operations, choose methods that minimize temporary collection creation to improve performance and reduce memory overhead.

Avoid creating unnecessary intermediate collections by:
- Using `diff()` instead of converting to Set and using `--` operator
- Leveraging iterators with filtering and mapping before final collection conversion
- Using Java streams with collectors when working with Java collections
- Choosing direct HashMap operations over collection conversions when appropriate

Examples:
```scala
// Inefficient - creates temporary Set
val result = partitionState.isr.asScala.map(_.toInt).toSet -- outOfSyncReplicaIds

// Better - uses diff to avoid temporary collection
val result = partitionState.isr.asScala.map(_.toInt).diff(outOfSyncReplicaIds)

// Alternative with iterator for complex operations
val result = current.isr.asScala.iterator.map(_.toInt).filter(_ != localBrokerId).to(Set)

// Java stream approach
val result = current.isr.stream().filter(isr => isr != localBrokerId).collect(Collectors.toUnmodifiableSet).asScala
```

This optimization reduces algorithmic complexity by eliminating unnecessary O(n) collection creation steps and improves memory efficiency in data structure operations.