---
title: Clear variable naming
description: Use descriptive, unambiguous variable and function names that clearly
  convey their purpose and avoid conflicts with Python built-ins or Home Assistant
  conventions.
repository: home-assistant/core
label: Naming Conventions
language: Python
comments_count: 8
repository_stars: 80450
---

Use descriptive, unambiguous variable and function names that clearly convey their purpose and avoid conflicts with Python built-ins or Home Assistant conventions.

**Key Guidelines:**
- Avoid overriding Python built-in names like `id`, `list`, `type`
- Use descriptive names that prevent confusion about functionality
- Follow Home Assistant naming conventions for entities and translation keys
- Avoid unnecessary prefixes in unique identifiers

**Examples:**

```python
# Bad: Overrides Python built-in
@dataclass
class RedgtechDevice:
    id: str  # Conflicts with built-in id() function

# Good: Use descriptive alternative
@dataclass
class RedgtechDevice:
    unique_id: str

# Bad: Ambiguous function name
class VolvoSensorDescription:
    is_available: Callable[[Vehicle], bool] = lambda _: True

# Good: Clear, specific name
class VolvoSensorDescription:
    supported_fn: Callable[[Vehicle], bool] = lambda _: True

# Bad: Unnecessary prefix in unique ID
self._attr_unique_id = f"fluss_{device['deviceId']}"

# Good: Clean unique ID (domain provides namespace)
self._attr_unique_id = str(device["deviceId"])

# Bad: Confusing field duplication
class VolvoEntityDescription:
    key: str
    api_field: str  # Same as key but camelCase

# Good: Use key directly or choose one clear name
class VolvoEntityDescription:
    key: str  # Use this for both purposes
```

**Translation Keys:** Use lowercase, snake_case format consistently:
```python
# Bad: Mixed case
translation_key="powerLevel"

# Good: Snake case
translation_key="power_level"
```

This prevents runtime errors, improves code readability, and ensures consistency with Home Assistant's established patterns.