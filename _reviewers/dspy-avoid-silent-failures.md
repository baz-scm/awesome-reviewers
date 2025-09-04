---
title: avoid silent failures
description: Always provide clear feedback when operations fail, even when continuing
  with fallbacks or alternative approaches. Silent failures make debugging extremely
  difficult and can lead to unexpected behavior in production systems.
repository: stanfordnlp/dspy
label: Error Handling
language: Python
comments_count: 9
repository_stars: 27813
---

Always provide clear feedback when operations fail, even when continuing with fallbacks or alternative approaches. Silent failures make debugging extremely difficult and can lead to unexpected behavior in production systems.

Key practices:
1. **Optional dependencies**: Wrap imports in try-except blocks but defer the error until actual usage, not at module level
2. **Operation failures**: Log warnings or raise informative exceptions instead of silently continuing
3. **Fallback scenarios**: When falling back to alternative approaches, log the reason for the fallback
4. **Parsing errors**: Provide specific error messages rather than generic exception handling

Example of proper optional dependency handling:
```python
# Good - defer error until usage
try:
    import optional_library
except ImportError:
    optional_library = None

def use_optional_feature():
    if optional_library is None:
        raise ImportError("optional_library is required for this feature. Install with: pip install optional_library")
    return optional_library.do_something()

# Bad - fails at import time
import optional_library  # This breaks if not installed
```

Example of proper fallback with feedback:
```python
# Good - inform about fallback
try:
    result = primary_operation()
except SpecificError as e:
    logger.warning(f"Primary operation failed: {e}. Falling back to alternative.")
    result = fallback_operation()

# Bad - silent fallback
try:
    result = primary_operation()
except:
    result = fallback_operation()  # No indication why fallback was used
```

This approach ensures that failures are visible to developers and operators, making systems more maintainable and debuggable.