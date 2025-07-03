---
title: Type-appropriate default values
description: Initialize variables with type-appropriate default values to prevent
  type errors and null reference exceptions during operations. When a variable is
  expected to hold a collection type (list, dictionary, set), use the corresponding
  empty collection (`[]`, `{}`, `set()`) rather than other falsy values like `None`
  or empty strings.
repository: kubeflow/kubeflow
label: Null Handling
language: Python
comments_count: 2
repository_stars: 15064
---

Initialize variables with type-appropriate default values to prevent type errors and null reference exceptions during operations. When a variable is expected to hold a collection type (list, dictionary, set), use the corresponding empty collection (`[]`, `{}`, `set()`) rather than other falsy values like `None` or empty strings.

For example, instead of:
```python
conditions = notebook.get("status", {}).get("conditions", "")
# Using "" as default for a variable that should be a list is problematic
if some_condition:
    conditions.append(new_item)  # This will fail if conditions is ""
```

Use type-appropriate defaults:
```python
conditions = notebook.get("status", {}).get("conditions", [])
# Using [] as default ensures the variable is always a list
if some_condition:
    conditions.append(new_item)  # This will work regardless
```

For complex data structures like dictionaries passed as parameters, consider adding type hints or documentation that clearly defines the expected structure, including which fields are optional vs. required. This helps prevent null reference errors when accessing dictionary keys.
