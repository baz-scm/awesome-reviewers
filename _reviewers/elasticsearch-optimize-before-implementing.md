---
title: Optimize before implementing
description: 'Before implementing algorithms, evaluate their efficiency implications,
  especially for operations that may be executed frequently or with large datasets.
  Consider:'
repository: elastic/elasticsearch
label: Algorithms
language: Java
comments_count: 8
repository_stars: 73104
---

Before implementing algorithms, evaluate their efficiency implications, especially for operations that may be executed frequently or with large datasets. Consider:

- Time and space complexity in typical and worst-case scenarios
- Memory allocation patterns and potential object churn
- Opportunities to avoid redundant computations or unnecessary iterations
- Impact on existing optimization pipelines and future optimization opportunities

Document algorithmic decisions and assumptions with clear comments. Flag potential future optimizations with TODO comments that explain the intended improvement.

For iterators and query processing, implement early termination strategies where possible:

```java
// Consider if we can skip entire ranges when we know no matches are possible
if (value < minTimestamp && allValuesInCurrentPrimarySort) {
    // We know we will not match any more documents in this primary sort
    approximation.match = Match.NO_AND_SKIP;
    return false;
}
```

For data structures, leverage existing infrastructure that handles memory tracking efficiently:

```java
// Use BlockHash to efficiently manage memory and circuit breaking
BlockHash blockHash = BlockHash.build(keys, blockFactory, breaker);
ObjectArray<Queue> queues = new ObjectArray<>(blockHash.capacity(), breaker);
```

When selecting nodes or distributing work, prefer approaches that minimize network traffic and object creation:

```java
// Iterate over eligible nodes (probably fewer) rather than all candidate nodes
return nodeIds.stream()
    .filter(nodeId -> candidateNodeIds.contains(nodeId))
    .collect(Collectors.toSet());
```
