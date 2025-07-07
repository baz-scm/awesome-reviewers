---
title: Follow Python naming conventions
description: 'Use consistent Python naming conventions to improve code readability
  and maintainability:


  1. Use snake_case for functions and variables:

  ```python

  # Bad'
repository: open-telemetry/opentelemetry-python
label: Naming Conventions
language: Python
comments_count: 5
repository_stars: 2061
---

Use consistent Python naming conventions to improve code readability and maintainability:

1. Use snake_case for functions and variables:
```python
# Bad
def setifnotnone(dic, key, value):
    
# Good
def set_if_not_none(dic, key, value):
```

2. Choose descriptive, semantic names that reflect purpose:
```python
# Bad
lst = []  # unclear what this list tracks

# Good
calls = []  # clearly indicates list tracks function calls
```

3. Maintain consistent naming with established patterns:
- Use standard type names (e.g., 'Attributes' instead of 'dict' for typed parameters)
- Follow existing naming patterns in the codebase (e.g., 'trace_exporter' vs 'span_exporter')
- Use semantic names that align with specifications and documentation

4. For internal/private variables, use single leading underscore and consistent suffixes:
```python
# Bad
self.currentValue = None
self.previous_cumulative_value = None

# Good
self._value = None
self._previous_value = None
```