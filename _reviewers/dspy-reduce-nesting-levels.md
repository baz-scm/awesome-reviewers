---
title: reduce nesting levels
description: Minimize nested conditional statements and complex control flow by using
  early returns, guard clauses, and default value patterns. This improves code readability
  and maintainability by reducing cognitive load.
repository: stanfordnlp/dspy
label: Code Style
language: Python
comments_count: 5
repository_stars: 27813
---

Minimize nested conditional statements and complex control flow by using early returns, guard clauses, and default value patterns. This improves code readability and maintainability by reducing cognitive load.

Use the `or` operator for default values instead of conditional checks:
```python
# Instead of:
if modules_to_serialize is not None:
    # process modules_to_serialize
else:
    modules_to_serialize = []

# Use:
modules_to_serialize = modules_to_serialize or []
```

Restructure conditional logic to reduce nesting:
```python
# Instead of:
result = dict(usage_entry2)
for k, v in usage_entry1.items():
    if isinstance(v, dict):
        if k in result:
            result[k] = self._merge_usage_entries(result[k], v)
        else:
            result[k] = dict(v) if isinstance(v, dict) else v
    else:
        result[k] = result[k] or 0
        result[k] += v if v else 0

# Use:
result = dict(usage_entry2)
for k, v in usage_entry1.items():
    current_v = result.get(k)
    if isinstance(v, dict):
        result[k] = self._merge_usage_entries(current_v, v)
    else:
        result[k] = current_v or 0
        result[k] += v if v else 0
```

For functions with many parameters, use multi-line formatting:
```python
# Instead of:
def __call__(self, lm: LM, lm_kwargs: dict[str, Any], signature: Type[Signature], demos: list[dict[str, Any]], inputs: dict[str, Any]) -> list[dict[str, Any]]:

# Use:
def __call__(
    self,
    lm: LM,
    lm_kwargs: dict[str, Any],
    signature: Type[Signature],
    demos: list[dict[str, Any]],
    inputs: dict[str, Any]
) -> list[dict[str, Any]]:
```