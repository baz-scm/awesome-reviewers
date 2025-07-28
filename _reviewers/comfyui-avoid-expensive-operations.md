---
title: avoid expensive operations
description: 'Identify and eliminate unnecessary expensive operations that can significantly
  impact performance. Common patterns to watch for include:


  1. **Unnecessary deep copying**: Instead of using `deepcopy()` on large objects,
  build new dictionaries with only the required values. For example, rather than `copy.deepcopy(self.history[key])`
  and then removing unwanted...'
repository: comfyanonymous/ComfyUI
label: Performance Optimization
language: Python
comments_count: 5
repository_stars: 83726
---

Identify and eliminate unnecessary expensive operations that can significantly impact performance. Common patterns to watch for include:

1. **Unnecessary deep copying**: Instead of using `deepcopy()` on large objects, build new dictionaries with only the required values. For example, rather than `copy.deepcopy(self.history[key])` and then removing unwanted fields, construct a new dictionary with only the needed data.

2. **Loop-invariant computations**: Move calculations that don't change between iterations outside of loops. For instance, if `interpolator(x)` produces the same result in every loop iteration, compute it once before the loop and store in a variable like `computed_spacing`.

3. **Missing caching for expensive operations**: Implement caching for frequently accessed heavy resources like models, file system operations, or computed values. Use model caches to "directly copy from cpu memory" rather than reloading from disk repeatedly.

4. **Redundant processing**: Avoid performing expensive operations on every function call when they could be done once or only when necessary. Check if computations can be moved to initialization or triggered only when input conditions change.

Before implementing expensive operations, consider: Is this computation necessary every time? Can the result be cached? Can the operation be moved outside a loop or conditional block? These optimizations often provide significant performance improvements with minimal code changes.