---
title: Optimize cache key design
description: Design cache keys to avoid performance pitfalls and ensure reliable cache
  behavior. Cache keys should be lightweight, hashable, and deterministic to prevent
  unnecessary cache misses and memory bloat.
repository: comfyanonymous/ComfyUI
label: Caching
language: Python
comments_count: 3
repository_stars: 83726
---

Design cache keys to avoid performance pitfalls and ensure reliable cache behavior. Cache keys should be lightweight, hashable, and deterministic to prevent unnecessary cache misses and memory bloat.

Key principles:
1. **Avoid large objects in cache keys** - Large values like images or models should not be part of the cache key as they bloat memory and slow down key comparison
2. **Ensure hashability** - Unhashable objects (like MODEL instances) in cache keys will cause nodes to always be considered 'dirty' and re-evaluated
3. **Use references over values** - Forward links to previous nodes rather than actual values when possible to keep keys lightweight
4. **Cache expensive key computations** - Store intermediate results of expensive signature calculations to avoid repeated work within execution cycles

Example of problematic cache key design:
```python
# BAD: Large image data becomes part of cache key
cache_key = (node_id, large_image_tensor, other_inputs)

# BAD: Unhashable model object causes cache misses  
cache_key = (node_id, model_instance, inputs)
```

Example of optimized cache key design:
```python
# GOOD: Use link references instead of actual values
if is_link(input_data):
    cache_key = (node_id, ("ANCESTOR", ancestor_index, socket))
else:
    cache_key = (node_id, input_data)  # Only for small, hashable data

# GOOD: Cache expensive signature computations
if node_id not in self.immediate_node_signature:
    self.immediate_node_signature[node_id] = self.compute_signature(node_id)
```

This approach ensures cache keys remain efficient while maintaining cache correctness, preventing both performance degradation and incorrect cache behavior.