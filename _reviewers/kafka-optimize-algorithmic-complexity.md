---
title: optimize algorithmic complexity
description: Replace inefficient algorithms with more optimal data structures and
  approaches to improve computational complexity. Look for opportunities to use appropriate
  data structures (like priority queues) instead of linear searches, avoid redundant
  iterations, and choose efficient traversal patterns.
repository: apache/kafka
label: Algorithms
language: Java
comments_count: 5
repository_stars: 30575
---

Replace inefficient algorithms with more optimal data structures and approaches to improve computational complexity. Look for opportunities to use appropriate data structures (like priority queues) instead of linear searches, avoid redundant iterations, and choose efficient traversal patterns.

Key optimization patterns to apply:

1. **Use priority queues for selection problems**: Instead of iterating through collections to find minimum/maximum elements, maintain a priority queue for O(log n) operations.

```java
// Instead of linear search through all members
final Member member = findMemberWithLeastLoad(allMembers, task, false);

// Use priority queue for efficient selection
PriorityQueue<ProcessState> processByLoad = new PriorityQueue<>(Comparator.comparingDouble(ProcessState::load));
processByLoad.addAll(localState.processIdToState.values());
ProcessState processWithLeastLoad = processByLoad.poll();
// Remember to add back after state changes
processByLoad.add(processWithLeastLoad);
```

2. **Avoid redundant iterations**: Use iterators or single-pass algorithms when possible to prevent multiple traversals of the same data.

```java
// Instead of filtering then iterating again
finalizedFeatureLevels.keySet().stream().filter(predicate).forEach(action);

// Use iterator for single-pass removal
var iter = finalizedFeatureLevels.keySet().iterator();
while (iter.hasNext()) {
    var featureName = iter.next();
    if (shouldRemove(featureName)) {
        removeFinalizedFeatureLevelMetric(featureName);
        iter.remove();
    }
}
```

3. **Choose efficient loop constructs**: Prefer simple loops over streams when performance is critical, especially for primitive operations.

```java
// Replace streams with loops for better performance
// replaced the Java Streams based iteration with a loop, since it's more efficient
for (Member member : prevMembers) {
    if (member.hasLeastLoad()) {
        return member;
    }
}
```

4. **Understand recursion bounds**: When using recursion, ensure it has predictable and bounded depth to avoid stack overflow while maintaining algorithmic clarity.

This approach reduces time complexity from O(n) linear searches to O(log n) priority queue operations and eliminates unnecessary object creation during iteration.