---
title: preserve exception context
description: When handling exceptions, preserve the original exception context and
  provide clear, actionable error information. Avoid creating new exceptions that
  lose important details from the original error, and replace generic error handling
  (like assertions) with specific, user-friendly messages.
repository: emcie-co/parlant
label: Error Handling
language: Python
comments_count: 5
repository_stars: 12205
---

When handling exceptions, preserve the original exception context and provide clear, actionable error information. Avoid creating new exceptions that lose important details from the original error, and replace generic error handling (like assertions) with specific, user-friendly messages.

Key practices:
- Re-raise original exceptions rather than creating new ones that lose context
- Use appropriate specific exception types rather than base exceptions when throwing
- Replace assertions with clear error messages that explain what went wrong
- Ensure proper error status codes are set in CLI applications

Example of what NOT to do:
```python
# Loses original exception context
except RateLimitError as e:
    raise RateLimitError(RATE_LIMIT_ERROR_MESSAGE, response=e.response, body=e.body)

# Generic assertion without clear message
assert condition or action
```

Example of better approach:
```python
# Preserve context with logging
except RateLimitError as e:
    logger.error(RATE_LIMIT_ERROR_MESSAGE)
    raise  # Re-raise original exception

# Clear error message
if not (condition or action):
    raise ValueError("At least one of --condition or --action is required")
    set_exit_status(1)
```

This ensures that debugging information is preserved while still providing clear feedback to users about what went wrong and how to fix it.