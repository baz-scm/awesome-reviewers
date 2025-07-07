---
title: Handle exceptions appropriately
description: 'When implementing error handling logic, be deliberate about which exception
  types you catch and where you handle them.


  1. **Catch `Exception`, not `BaseException`** - Classes that directly inherit from
  `BaseException` (like `GeneratorExit` or `KeyboardInterrupt`) are not technical
  errors and should generally propagate:'
repository: open-telemetry/opentelemetry-python
label: Error Handling
language: Python
comments_count: 5
repository_stars: 2061
---

When implementing error handling logic, be deliberate about which exception types you catch and where you handle them.

1. **Catch `Exception`, not `BaseException`** - Classes that directly inherit from `BaseException` (like `GeneratorExit` or `KeyboardInterrupt`) are not technical errors and should generally propagate:

```python
# Good
try:
    # operation that may fail
except Exception as exc:  # Only catches errors, not control flow exceptions
    record_error(exc)

# Bad
try:
    # operation that may fail
except BaseException as exc:  # Catches everything including KeyboardInterrupt
    record_error(exc)
```

2. **Handle exceptions at the appropriate layer** - Catch exceptions in the code that has the context to properly handle them:

```python
# Good: Handle file access errors in file-reading functions
def _read_file(file_path: str) -> Optional[bytes]:
    try:
        with open(file_path, "rb") as file:
            return file.read()
    except FileNotFoundError as e:
        logger.exception(f"Failed to read file: {e.filename}")
        return None

# Bad: Force higher-level code to handle file-specific errors
def _read_file(file_path: str) -> bytes:
    with open(file_path, "rb") as file:
        return file.read()
    # FileNotFoundError bubbles up to caller
```

3. **Preserve valuable error information** - When handling exceptions, ensure meaningful error details are preserved in logs or return values.

4. **Balance fail-fast and graceful degradation** - Consider the context:
   - For configuration errors during initialization, fail-fast can prevent harder-to-debug issues later
   - For runtime errors in production code, graceful degradation is often preferred to avoid service disruption