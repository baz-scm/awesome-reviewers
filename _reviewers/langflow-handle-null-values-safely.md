---
title: Handle null values safely
description: When handling potentially null or undefined values, implement explicit
  null checks and provide safe default values rather than allowing null values to
  propagate through the system. This prevents null reference errors and ensures predictable
  behavior.
repository: langflow-ai/langflow
label: Null Handling
language: Python
comments_count: 3
repository_stars: 111046
---

When handling potentially null or undefined values, implement explicit null checks and provide safe default values rather than allowing null values to propagate through the system. This prevents null reference errors and ensures predictable behavior.

Key practices:
- Use explicit null checks with early returns to safe defaults
- Make parameters optional with appropriate default values when the information may not always be available
- Provide meaningful default values (like empty lists or dictionaries) instead of None

Example from MultiselectInput validation:
```python
@field_validator("value", mode="before")
@classmethod
def validate_value(cls, v: Any, _info):
    # Handle None safely during construction
    if v is None:
        return []
    
    if not isinstance(v, list):
        msg = f"MultiselectInput value must be a list. Got: {type(v)}"
        raise TypeError(msg)
    # ... rest of validation
```

This pattern ensures that null values are caught early and converted to safe, usable defaults, preventing downstream null reference issues while maintaining clear error messages for invalid non-null values.