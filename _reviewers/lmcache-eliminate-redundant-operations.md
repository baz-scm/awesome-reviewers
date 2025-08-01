---
title: Eliminate redundant operations
description: Avoid unnecessary function calls, I/O operations, and redundant checks
  that can significantly impact performance. Look for opportunities to consolidate
  operations, remove duplicate work, and streamline execution paths.
repository: LMCache/LMCache
label: Performance Optimization
language: Python
comments_count: 5
repository_stars: 3800
---

Avoid unnecessary function calls, I/O operations, and redundant checks that can significantly impact performance. Look for opportunities to consolidate operations, remove duplicate work, and streamline execution paths.

Common patterns to watch for:
- Redundant function calls that could be eliminated or cached
- Unnecessary I/O operations like extra RPC calls or database queries  
- Duplicate checks or validations that serve the same purpose
- Inefficient loops that could be replaced with batch operations

Example improvements:
```python
# Instead of repeated append() calls and redundant checks:
if location not in key_mapping:
    key_mapping[location] = [key]
    start_mapping[location] = [start]
    end_mapping[location] = [end]
    continue
key_mapping[location].append(key)
start_mapping[location].append(start) 
end_mapping[location].append(end)

# Use efficient unpacking to avoid repeated operations:
if reordered_blocks:
    _, memory_objs, starts, ends = zip(*reordered_blocks)
    self.gpu_connector.batched_to_gpu(list(memory_objs), list(starts), list(ends), **kwargs)
```

```python
# Remove unnecessary I/O operations:
# Instead of: if self.exists_in_put_tasks(key) or self.contains(key):
# Just use: if self.exists_in_put_tasks(key):
# The contains() call adds unnecessary RPC or I/O overhead
```

Always question whether each operation is truly necessary and look for opportunities to batch, cache, or eliminate redundant work entirely.