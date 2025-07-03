---
title: Optimize iteration patterns
description: 'When iterating through collections, choose the most efficient iteration
  pattern based on what information you actually need. If you only need the elements
  without using their indices, use direct iteration instead of enumerate:'
repository: apache/mxnet
label: Algorithms
language: Python
comments_count: 6
repository_stars: 20801
---

When iterating through collections, choose the most efficient iteration pattern based on what information you actually need. If you only need the elements without using their indices, use direct iteration instead of enumerate:

```python
# Instead of this (inefficient):
for _, item in enumerate(collection):
    process(item)

# Do this (efficient and clearer):
for item in collection:
    process(item)
```

This optimization removes unnecessary index variable allocation and makes the code more readable. The principle applies to any iterative algorithm - don't compute values you won't use. Similarly, when testing object capabilities (like whether an object is iterable), check for specific attributes (`hasattr(obj, '__iter__')`) rather than calling functions that might have side effects like prefetching data.
