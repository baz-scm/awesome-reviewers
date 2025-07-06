---
title: Create demonstrative examples
description: 'Include clear, concise examples in documentation that effectively demonstrate
  functionality. Follow these principles for better documentation examples:'
repository: pola-rs/polars
label: Documentation
language: Python
comments_count: 3
repository_stars: 34296
---

Include clear, concise examples in documentation that effectively demonstrate functionality. Follow these principles for better documentation examples:

1. Include specific examples for each new parameter or feature
2. Show both input and output when demonstrating transformations
3. Use examples that show meaningfully different results to illustrate behavior
4. Keep examples simple but comprehensive enough to demonstrate functionality

Example of an effective documentation example:

```python
# Good example - shows different results with before/after
from datetime import datetime
s = pl.Series("datetime", [datetime(2024, 1, 1), datetime(2024, 1, 2)])

# Original series
print(s)
# shape: (2,)
# Series: 'datetime' [datetime[μs]]
# [
#     2024-01-01 00:00:00
#     2024-01-02 00:00:00
# ]

# After replacement - shows varied results
result = s.dt.replace(year=2022)
print(result)
# shape: (2,)
# Series: 'datetime' [datetime[μs]]
# [
#     2022-01-01 00:00:00
#     2022-01-02 00:00:00
# ]
```

Users learn more effectively from examples than from descriptions alone. Well-constructed examples that demonstrate real usage patterns significantly improve API usability.