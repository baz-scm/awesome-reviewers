---
title: Normalize configuration parameters
description: Always normalize configuration inputs (especially environment variables)
  by removing whitespace and applying consistent case transformation before processing
  them. This prevents unexpected behaviors caused by insignificant variations in input
  format.
repository: pytorch/pytorch
label: Configurations
language: Python
comments_count: 4
repository_stars: 91345
---

Always normalize configuration inputs (especially environment variables) by removing whitespace and applying consistent case transformation before processing them. This prevents unexpected behaviors caused by insignificant variations in input format.

For environment variables:
```python
# Good practice
env_value = os.environ.get('TORCH_CONFIG_VAR', None)
if env_value:
    env_value = env_value.strip().lower()
    # Now process with normalized value
```

For configuration dictionaries, make sure keys are properly normalized if case-insensitive matching is required.

Additionally:
1. Don't raise errors for unrecognized configuration parameters when they may be valid for other components or backends - skip or ignore them instead.
2. In documentation, maintain proper syntax for environment variables (e.g., `PYTORCH_TUNABLEOP_ENABLED=1` without spaces).
3. Consider configuration granularity - determine whether a global configuration is sufficient or if per-site configuration offers better flexibility for your specific use case.