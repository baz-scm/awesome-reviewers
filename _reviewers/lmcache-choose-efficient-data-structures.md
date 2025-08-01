---
title: Choose efficient data structures
description: Select appropriate built-in data structures and algorithmic patterns
  that eliminate manual checks and reduce code complexity. This improves both performance
  and maintainability by leveraging Python's optimized implementations.
repository: LMCache/LMCache
label: Algorithms
language: Python
comments_count: 3
repository_stars: 3800
---

Select appropriate built-in data structures and algorithmic patterns that eliminate manual checks and reduce code complexity. This improves both performance and maintainability by leveraging Python's optimized implementations.

Key principles:
1. **Use defaultdict instead of manual key existence checks** - Replace patterns like `if key not in dict: dict[key] = []` with `defaultdict(list)`
2. **Try direct operations before fallback logic** - Attempt the primary algorithm first, then handle edge cases, rather than pre-checking conditions
3. **Leverage built-in data structure behaviors** - Use data structures that naturally handle your use case rather than implementing the logic manually

Example from the codebase:
```python
# Instead of manual key checking:
if location not in key_mapping:
    key_mapping[location] = [key]
    start_mapping[location] = [start] 
    end_mapping[location] = [end]

# Use defaultdict to eliminate the check:
from collections import defaultdict
block_mapping: defaultdict = defaultdict(list)
block_mapping[location].append((key, start, end))
```

For memory management algorithms, try allocation first before implementing eviction logic:
```python
# Try direct allocation first
memory_obj = self.memory_allocator.allocate(shape, dtype)
if memory_obj is None:
    # Then implement eviction logic
    self._evict_and_retry_allocation(shape, dtype)
```

This approach reduces branching, leverages optimized implementations, and makes code more readable and less error-prone.