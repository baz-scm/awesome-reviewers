---
title: prefer simple readable code
description: 'Write code that prioritizes clarity and simplicity over cleverness.
  This improves maintainability and reduces cognitive load for other developers.


  Key practices:'
repository: python-poetry/poetry
label: Code Style
language: Python
comments_count: 10
repository_stars: 33496
---

Write code that prioritizes clarity and simplicity over cleverness. This improves maintainability and reduces cognitive load for other developers.

Key practices:
- Use positive conditionals instead of negative ones with empty blocks
- Extract inline conditions to named variables when they improve readability
- Avoid unnecessary complexity like functools.partial when simpler alternatives exist
- Inline variables that are only used once to reduce noise
- Use explicit parameter names for boolean arguments
- Keep methods concise and focused on a single responsibility
- Use modern Python idioms like pathlib's `/` operator and `or` for conditional assignment

Example of improvements:
```python
# Instead of negative conditional with empty block
if not condition:
    pass
else:
    do_something()

# Prefer positive conditional
if condition:
    do_something()

# Instead of inline complex condition
if not username and not password:
    return None

# Extract to named variable for clarity  
has_credentials = username or password
if not has_credentials:
    return None

# Instead of nameless boolean parameter
return self._handle_install(True)

# Use explicit parameter name
return self._handle_install(with_synchronization=True)
```

The goal is code that can be understood at a glance without requiring mental gymnastics to parse complex logic or unclear intentions.