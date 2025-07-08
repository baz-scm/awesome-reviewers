---
title: Safe attribute access patterns
description: Implement consistent patterns for safely accessing potentially null or
  undefined attributes and dictionary values. This prevents runtime errors and makes
  code more robust.
repository: prowler-cloud/prowler
label: Null Handling
language: Python
comments_count: 5
repository_stars: 11834
---

Implement consistent patterns for safely accessing potentially null or undefined attributes and dictionary values. This prevents runtime errors and makes code more robust.

Key patterns to follow:

1. For dictionary access, use .get() with default value:
```python
# Instead of dict["key"]
location = project_info["source"].get("location", "")
```

2. For object attributes, use getattr():
```python
# Instead of obj.attribute
name = getattr(contact, "name", "default")
```

3. For complex fallback chains, use clear progressive checks:
```python
# Multiple fallbacks with clear intent
resource_id = (
    explicit_id or 
    getattr(resource_metadata, "id", None) or 
    getattr(resource_metadata, "name", None) or 
    ""
)
```

4. For nested null checks, combine patterns:
```python
# Safe nested access
is_mfa_capable = getattr(registration_details.get(user.id), "is_mfa_capable", False)
```

These patterns ensure graceful handling of missing values while maintaining code readability. Choose the appropriate pattern based on the data structure you're working with (dictionary vs object) and the complexity of the fallback logic needed.