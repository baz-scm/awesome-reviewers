---
title: Choose data structures wisely
description: Select data structures based on your specific access patterns and performance
  requirements. Using the right data structure can simplify your code and improve
  performance significantly.
repository: open-telemetry/opentelemetry-python
label: Algorithms
language: Python
comments_count: 4
repository_stars: 2061
---

Select data structures based on your specific access patterns and performance requirements. Using the right data structure can simplify your code and improve performance significantly.

For queue-like operations where you need to add/remove from both ends efficiently, use specialized collections like `deque` instead of plain lists:

```python
# Instead of this:
self._metrics_to_export = []
# ...later...
self._metrics_to_export.append(metric_records)
# ...and in another method...
self._metrics_to_export.remove(metric_batch)  # Inefficient for large lists

# Use this:
from collections import deque
self._metrics_to_export = deque()
# ...later...
self._metrics_to_export.append(metric_records)
# ...and in another method...
metric_batch = self._metrics_to_export.popleft()  # O(1) operation
```

When working with collections:
1. Never modify a collection while iterating over it - this can cause subtle bugs and unpredictable behavior
2. Consider the order of operations in algorithms carefully - even small changes like incrementing a counter before vs. after an operation can affect correctness
3. When using circular buffers or specialized data structures, provide helper methods to convert between internal representations and standard formats

For example, when iterating and modifying:
```python
# Instead of this:
for metric_batch in self._metrics_to_export:
    # process metric_batch
    self._metrics_to_export.remove(metric_batch)  # DANGER! Modifying during iteration

# Use this:
while self._metrics_to_export:
    metric_batch = self._metrics_to_export.popleft()
    # process metric_batch
```