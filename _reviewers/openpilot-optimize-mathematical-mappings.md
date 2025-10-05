---
title: optimize mathematical mappings
description: Use consistent units and data representations throughout mathematical
  calculations to avoid unnecessary computational overhead. When working with value
  ranges, prefer direct mathematical mappings over multiple conversions, and leverage
  utility functions for range transformations.
repository: commaai/openpilot
label: Algorithms
language: Other
comments_count: 2
repository_stars: 58214
---

Use consistent units and data representations throughout mathematical calculations to avoid unnecessary computational overhead. When working with value ranges, prefer direct mathematical mappings over multiple conversions, and leverage utility functions for range transformations.

For example, instead of converting between different units multiple times:
```cpp
// Avoid multiple conversions
int ir_percent = util::map_val(static_cast<int>(ir_pwr), 0, static_cast<int>(100*MAX_IR_POWER), 0, 100);

// Better: work in consistent units, then map once
int value = util::map_val(std::clamp(percent, 0, 100), 0, 100, 0, 255);
```

This approach reduces computational complexity, minimizes floating-point precision errors, and makes the code more maintainable by establishing clear data flow patterns. Choose the most natural unit for your domain and stick with it throughout the calculation pipeline.