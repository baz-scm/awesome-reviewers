---
title: Raise exceptions properly
description: Always ensure exceptions are properly raised and propagated rather than
  being logged and swallowed. Avoid patterns where errors are caught, logged, and
  then execution continues normally, as this can hide critical failures from calling
  code.
repository: Unstructured-IO/unstructured
label: Error Handling
language: Python
comments_count: 5
repository_stars: 12116
---

Always ensure exceptions are properly raised and propagated rather than being logged and swallowed. Avoid patterns where errors are caught, logged, and then execution continues normally, as this can hide critical failures from calling code.

Key principles:
1. **Re-raise after logging**: When catching exceptions for logging purposes, always re-raise them so calling code can handle the failure appropriately
2. **Avoid returning error strings**: Don't return error messages as strings from functions - raise exceptions instead so they can be properly handled by the caller
3. **Use specific exception handling**: Avoid overly broad `except Exception:` blocks that might hide unexpected errors. When you must use broad handlers, ensure error details are preserved and re-raised
4. **Control exception chaining**: Use `from None` when re-raising exceptions to prevent sensitive data (like file contents) from being captured in exception chains

Example of proper error handling:
```python
# Bad - logs error but continues execution
try:
    result = risky_operation()
except Exception as e:
    logger.error(f"Error occurred: {e}")
    # Execution continues, error is hidden

# Good - logs error and re-raises
try:
    result = risky_operation()
except Exception as e:
    logger.error(f"Error occurred: {e}")
    raise  # or raise specific exception type

# Good - prevents data leakage in exception chains
try:
    file_text = byte_data.decode(encoding)
except (UnicodeDecodeError, UnicodeError):
    raise UnprocessableEntityError(
        f"File encoding detection failed: detected '{encoding}' but decode failed."
    ) from None  # Prevents original exception with file data from being chained
```

This ensures that failures are communicated to calling code and can be handled appropriately, rather than being silently ignored.