---
title: prefer explicit readability
description: Choose explicit, readable code constructs over "clever" or overly complex
  ones. Complex functional programming constructs, intricate ternary operators, and
  large list comprehensions can make code harder to understand and maintain.
repository: docker/compose
label: Code Style
language: Python
comments_count: 3
repository_stars: 35858
---

Choose explicit, readable code constructs over "clever" or overly complex ones. Complex functional programming constructs, intricate ternary operators, and large list comprehensions can make code harder to understand and maintain.

**Prefer explicit conditionals:**
```python
# Instead of:
msg = not silent and 'Pulling' or None

# Use:
msg = 'Pulling' if not silent else None
```

**Avoid complex functional constructs when simpler alternatives exist:**
```python
# Instead of reduce() with mixed return types:
return reduce(combine_configs, configs + [None])

# Use explicit loops:
result = None
for config in configs:
    result = combine_configs(result, config)
return result
```

**Break down complex list comprehensions:**
```python
# Instead of nested, multi-line list comprehensions:
service_names = [
    service.name
    for service in self.services
    if 'profiles' not in service.options or [
        e for e in service.options.get('profiles')
        if e in enabled_profiles
    ]
]

# Extract to a clear method:
service_names = [
    service.name
    for service in self.services
    if service.enabled_for_profiles(enabled_profiles)
]
```

This approach makes code easier to debug, test, and understand for team members, reducing cognitive load during code reviews and maintenance.