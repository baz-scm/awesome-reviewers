---
title: Simple defaults, flexible overrides
description: Design APIs with intuitive defaults for common use cases while providing
  specialized options for edge cases. This approach makes your API approachable for
  most users while maintaining flexibility for advanced scenarios.
repository: pydantic/pydantic
label: API
language: Python
comments_count: 4
repository_stars: 24377
---

Design APIs with intuitive defaults for common use cases while providing specialized options for edge cases. This approach makes your API approachable for most users while maintaining flexibility for advanced scenarios.

**Key principles:**
1. Identify the most common use patterns and optimize for them
2. Consolidate related parameters when they typically have the same value
3. Provide escape hatches for complex cases without complicating the common path
4. Use sensible defaults that work for most users

For example, instead of having separate configuration parameters that are usually set to identical values:

```python
# Problematic design - requires duplicate settings for common case
config = ConfigDict(
    val_date_or_time_unit='milliseconds',
    ser_date_or_time_unit='milliseconds',
)

# Better design
config = ConfigDict(
    date_or_time_unit='milliseconds',  # Applies to both validation and serialization
    # Add specific overrides only when needed:
    val_date_or_time_unit_override=None,  # Only set when different from common setting
)
```

Similarly, when designing validators or constraint systems, provide high-level simple APIs for common cases, with options to bypass default behavior when needed (like the `check_unsupported_field_info_attributes=False` parameter that allows silencing warnings in specific contexts).

For URL schemes and other extensible systems, include the most commonly used variants by default while allowing extension for specialized cases.