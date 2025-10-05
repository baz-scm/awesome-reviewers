---
title: optimize data structure selection
description: Choose data structures and algorithms based on their computational complexity
  and access patterns rather than convenience. Consider performance implications when
  selecting between alternatives.
repository: commaai/openpilot
label: Algorithms
language: Python
comments_count: 4
repository_stars: 58214
---

Choose data structures and algorithms based on their computational complexity and access patterns rather than convenience. Consider performance implications when selecting between alternatives.

Key principles:
1. **Match data structure to access patterns**: Use `np.array` instead of Python lists when performing mathematical operations, as numpy can optimize operations internally without type conversion overhead.

2. **Choose algorithms based on constraints**: Select streaming algorithms when memory usage matters more than speed, and batch algorithms when speed is critical and memory is available.

3. **Avoid expensive operations in hot paths**: Replace costly operations like `inspect.getmodule()` with simpler alternatives such as direct I/O operations or cached lookups.

4. **Make implementations algorithm-agnostic**: Design interfaces that work with different underlying implementations (e.g., `queue.clear()` vs creating new queue instances).

Example from the codebase:
```python
# Before: Python list requiring conversion
self.posenet_stds = [POSENET_STD_INITIAL_VALUE] * (POSENET_STD_HIST_HALF * 2)
old_mean = np.mean(self.posenet_stds[:POSENET_STD_HIST_HALF])  # Converts list to array internally

# After: Direct numpy array for better performance
self.posenet_stds = np.array([POSENET_STD_INITIAL_VALUE] * (POSENET_STD_HIST_HALF * 2))
old_mean = np.mean(self.posenet_stds[:POSENET_STD_HIST_HALF])  # No conversion needed
```

When choosing between algorithmic approaches, document the trade-offs. For instance, `zstd.decompress()` is faster for files with size headers, while streaming decompression handles variable-size data but with slight performance cost. Choose based on your data characteristics and constraints.