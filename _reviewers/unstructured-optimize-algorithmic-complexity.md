---
title: optimize algorithmic complexity
description: When implementing algorithms, prioritize performance by avoiding unnecessary
  computations and choosing efficient approaches. Consider algorithmic complexity
  early in design and look for opportunities to eliminate redundant operations or
  expensive calculations when simpler alternatives exist.
repository: Unstructured-IO/unstructured
label: Algorithms
language: Python
comments_count: 4
repository_stars: 12116
---

When implementing algorithms, prioritize performance by avoiding unnecessary computations and choosing efficient approaches. Consider algorithmic complexity early in design and look for opportunities to eliminate redundant operations or expensive calculations when simpler alternatives exist.

Key strategies include:
- **Early termination**: Skip expensive operations when conditions make them unnecessary, like checking file size ratios before running costly distance calculations
- **Prevent rather than filter**: Design algorithms to avoid creating unwanted data rather than filtering it out later
- **Eliminate duplicate work**: Avoid parsing or processing the same data multiple times in a pipeline
- **Profile when uncertain**: When multiple approaches have unclear performance trade-offs, measure and compare them

Example from the codebase:
```python
# Instead of always running expensive Levenshtein distance:
if 0.5 < len(output_cct.encode()) / len(source_cct.encode()) < 2.0:
    accuracy = round(calculate_accuracy(output_cct, source_cct, weights), 3)
else:
    accuracy = 0.01  # Skip expensive calculation when files differ wildly
```

This approach prevents performance bottlenecks and ensures algorithms scale appropriately with input size.