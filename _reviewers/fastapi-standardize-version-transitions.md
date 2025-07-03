---
title: Standardize version transitions
description: 'When supporting multiple library versions or preparing for version deprecation
  in configuration-dependent code, use standardized TODO comments with consistent
  formatting. Always include a space after the # symbol and use the prefix "TODO:"
  to ensure comments can be found with standard search tools.'
repository: fastapi/fastapi
label: Configurations
language: Python
comments_count: 3
repository_stars: 86871
---

When supporting multiple library versions or preparing for version deprecation in configuration-dependent code, use standardized TODO comments with consistent formatting. Always include a space after the # symbol and use the prefix "TODO:" to ensure comments can be found with standard search tools.

Example:
```python
def pydantic_snapshot(
    *,
    v2: Snapshot,
    v1: Snapshot,  # TODO: remove v1 argument when deprecating Pydantic v1
):
    # Version-specific implementation
    if PYDANTIC_V2:
        return v2
    else:
        return v1
```

This practice helps teams track configuration-dependent code that will require updates during dependency upgrades, making version transitions smoother and more systematic. It also ensures that version-specific code paths are clearly documented and can be easily located when performing major configuration changes.