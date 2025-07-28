---
title: Review configuration constants regularly
description: Configuration constants and mappings require regular maintenance to stay
  aligned with evolving platform capabilities. Outdated configurations can introduce
  unnecessary complexity, while incomplete mappings can cause functionality loss.
repository: home-assistant/core
label: Configurations
language: Other
comments_count: 2
repository_stars: 80450
---

Configuration constants and mappings require regular maintenance to stay aligned with evolving platform capabilities. Outdated configurations can introduce unnecessary complexity, while incomplete mappings can cause functionality loss.

Periodically audit configuration constants to:
1. Remove redundant manual conversions when automatic alternatives become available
2. Ensure mapping dictionaries are complete for all supported values
3. Update configurations when underlying platform capabilities change

Example of configuration constants that need review:
```python
# Before: Manual unit conversion (now redundant)
DEVICE_CLASS_UNITS = {
    "current": "mA",  # Manual conversion from A to mA
}

# After: Let platform handle automatic conversions
DEVICE_CLASS_UNITS = {
    "current": "A",   # Use standard unit, let platform convert
}

# Ensure complete mappings to avoid losing device classes
DEVICE_CLASS_UNITS = {
    "current": "A",
    "duration": "min",  # Add missing mappings
    "voltage": "V",
}
```

This prevents bugs where valid configurations are incorrectly removed due to incomplete mappings, and eliminates maintenance overhead from obsolete manual conversions.