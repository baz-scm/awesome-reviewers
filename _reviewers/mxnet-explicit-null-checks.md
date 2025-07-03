---
title: Explicit null checks
description: Always use explicit null checks (`value is None` or `value is not None`)
  rather than implicit truthiness evaluations when testing for null/None values. Implicit
  boolean checks can invoke `__bool__` methods leading to unexpected behavior.
repository: apache/mxnet
label: Null Handling
language: Python
comments_count: 4
repository_stars: 20801
---

Always use explicit null checks (`value is None` or `value is not None`) rather than implicit truthiness evaluations when testing for null/None values. Implicit boolean checks can invoke `__bool__` methods leading to unexpected behavior.

**Do this:**
```python
# Explicitly check if out is not None
if out is not None:
    # Use out
    process(out)
```

**Not this:**
```python
# Don't rely on truthiness which may call __bool__
if out:
    # May not behave as expected if __bool__ is implemented
    process(out)
```

For complex types that can represent optional values, use proper optional type wrappers:

In C++:
```cpp
// Use optional wrappers for nullable types
'float or None': 'dmlc::optional<float>'  // Instead of just 'mx_float'
```

When handling values that might have multiple return types or be null:
```python
# Check the specific type before processing
if isinstance(out, NDArrayBase):
    return out
return list(out)  # Convert if needed
```
