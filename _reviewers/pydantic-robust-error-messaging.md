---
title: Robust error messaging
description: 'Create clear, specific, and actionable error messages that help users
  understand and resolve issues, while implementing defensive error handling to maintain
  system integrity. Follow these principles:'
repository: pydantic/pydantic
label: Error Handling
language: Python
comments_count: 5
repository_stars: 24377
---

Create clear, specific, and actionable error messages that help users understand and resolve issues, while implementing defensive error handling to maintain system integrity. Follow these principles:

1. **Write user-focused error messages** that explain what went wrong and how to fix it
2. **Use defensive error handling** with specific exception types and cleanup mechanisms
3. **Defer expensive error computations** until actually needed

Example of good error handling:

```python
def validate_path(path: Path) -> Path:
    try:
        # Check path length before accessing filesystem
        if isinstance(path, PosixPath) and path.parent.exists():
            try:
                if os.statvfs(path.parent).f_namemax < len(path.name):
                    raise PydanticCustomError('path_too_long', 'Path name is too long')
            except OSError:
                # Handle specific error when path is inaccessible
                raise PydanticCustomError('path_error', f'Path "{path}" cannot be accessed')
                
        if not path.exists():
            # Specific, actionable error message
            raise PydanticCustomError('path_not_found', f'Path "{path}" does not exist')
            
        return path
    except Exception as e:
        # Preserve original error information while adding context
        raise ValueError(f"Invalid path: {e}") from e
```

When modifying functions or objects that might raise exceptions, always use try/finally blocks to ensure cleanup:

```python
original_qualname = function.__qualname__
try:
    # Potentially risky modifications
    function.__qualname__ = new_qualname
    # Additional operations...
    return function
finally:
    # Ensure cleanup on failure
    if some_error_condition:
        function.__qualname__ = original_qualname
```

For performance-critical code, defer expensive error message construction:

```python
# Instead of computing expensive messages upfront:
# error_msg = f"Complex {expensive_calculation()} message"
# raise ValueError(error_msg)

# Use a lazy approach:
def get_error_message():
    return f"Complex {expensive_calculation()} message"

# Only computed when an error actually occurs
if error_condition:
    raise ValueError(get_error_message())
```