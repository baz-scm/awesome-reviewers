---
title: Verify union attribute access
description: When working with union types in Python, always verify that all components
  of the union have the attributes you're trying to access or modify. Failure to do
  so can lead to runtime errors when the code attempts to access undefined attributes.
repository: astral-sh/ruff
label: Null Handling
language: Markdown
comments_count: 3
repository_stars: 40619
---

When working with union types in Python, always verify that all components of the union have the attributes you're trying to access or modify. Failure to do so can lead to runtime errors when the code attempts to access undefined attributes.

For attribute access on unions:
1. Check that all possible types in the union support the attribute you're accessing
2. Use conditional checks or type guards to narrow the union before accessing type-specific attributes
3. Handle the case where an attribute might be missing

```python
from typing import Union

class A:
    pass  # No 'x' attribute

class B:
    x: int  # Has 'x' attribute

# Unsafe pattern - might cause runtime errors:
def unsafe(obj: Union[A, B]):
    obj.x = 42  # Error: possibly-unbound-attribute
    
# Safe pattern - check type first:
def safe(obj: Union[A, B]):
    if isinstance(obj, B):
        obj.x = 42  # Safe, we've verified this is type B
        
# Alternative safe pattern - use hasattr:
def also_safe(obj: Union[A, B]):
    if hasattr(obj, "x"):
        obj.x = 42  # Safe, we've verified attribute exists
```

Similarly, when using the `del` statement, track deleted variables carefully and avoid accessing them after deletion to prevent "unresolved-reference" errors.