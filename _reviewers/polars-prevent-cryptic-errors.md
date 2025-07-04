---
title: Prevent cryptic errors
description: Always implement proper validation and type checking to prevent cryptic
  error messages. When errors do occur, provide clear, actionable guidance for resolution.
repository: pola-rs/polars
label: Error Handling
language: Python
comments_count: 4
repository_stars: 34296
---

Always implement proper validation and type checking to prevent cryptic error messages. When errors do occur, provide clear, actionable guidance for resolution.

Key practices:
1. Use exact instance checking rather than isinstance() when needed to avoid attribute errors:
```python
# Prefer this
if isinstance(path, io.BytesIO):
    target = path
# Over potentially error-prone checks that could lead to attribute errors
```

2. Place input validation at appropriate scope levels to catch errors early:
```python
# Validate inputs early with helpful error messages
if len(exprs) == 1 and isinstance(exprs[0], Mapping):
    msg = (
        "Cannot pass a dictionary as a single positional argument.\n"
        "If you merely want the *keys*, use:\n"
        "  • df.method(*your_dict.keys())\n"
        "If you need the key–value pairs, use one of:\n"
        "  • unpack as keywords:    df.method(**your_dict)\n"
        "  • build expressions:     df.method(expr.alias(k) for k, expr in your_dict.items())"
    )
    raise TypeError(msg)
```

3. Consider returning None instead of raising exceptions for non-critical failures to allow more consistent error handling by callers.

4. Leverage built-in language error mechanisms when appropriate rather than implementing custom error checking that duplicates existing functionality.