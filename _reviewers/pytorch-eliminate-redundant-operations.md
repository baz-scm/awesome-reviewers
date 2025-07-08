---
title: Eliminate redundant operations
description: "Avoid unnecessary operations that can impact performance. This includes:\n\
  \n1. Redundant data transformations:\n   - Load data directly from sources instead\
  \ of creating temporary copies"
repository: pytorch/pytorch
label: Performance Optimization
language: Python
comments_count: 4
repository_stars: 91345
---

Avoid unnecessary operations that can impact performance. This includes:

1. Redundant data transformations:
   - Load data directly from sources instead of creating temporary copies
   - Reuse existing transformed data rather than recreating it
   - Avoid unnecessary type conversions

2. Minimize attribute lookups and string operations:
   - Cache frequently accessed attributes
   - Avoid redundant string conversions, especially in logging

Example of improvements:

```python
# Bad - Unnecessary string conversion and temporary storage
content = path.read_text(encoding="utf-8")
pyproject = tomllib.loads(content)

# Good - Direct loading
pyproject = tomllib.loads(path.read_text(encoding="utf-8"))

# Bad - Redundant str conversion in logging
log.debug("Selected choice: %s", str(node))

# Good - Let logging handle the conversion
log.debug("Selected choice: %s", node)
```

These optimizations are particularly important in performance-critical paths and frequently executed code sections.