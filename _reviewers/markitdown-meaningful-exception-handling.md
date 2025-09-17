---
title: meaningful exception handling
description: Exception handling should provide meaningful feedback and use appropriate
  exception types rather than failing silently or relying on fragile string-based
  checks. Avoid catching exceptions without proper logging, user feedback, or recovery
  mechanisms. Use built-in Python exceptions when available instead of creating custom
  ones unnecessarily.
repository: microsoft/markitdown
label: Error Handling
language: Python
comments_count: 3
repository_stars: 76602
---

Exception handling should provide meaningful feedback and use appropriate exception types rather than failing silently or relying on fragile string-based checks. Avoid catching exceptions without proper logging, user feedback, or recovery mechanisms. Use built-in Python exceptions when available instead of creating custom ones unnecessarily.

Key practices:
- Never catch exceptions silently - always log warnings or provide user feedback
- Use built-in exception types (like FileNotFoundError) instead of custom exceptions when appropriate  
- Avoid checking exception messages with string comparisons as they can be fragile across versions or locales
- Provide clear error context to help with debugging

Example of problematic silent handling:
```python
try:
    result = subprocess.run(libreoffice_command, capture_output=True, text=True)
    # ... process result
except Exception as _:
    # Silent failure - no logging or user feedback
    pass
```

Better approach with meaningful handling:
```python
try:
    result = subprocess.run(libreoffice_command, capture_output=True, text=True)
    # ... process result  
except subprocess.SubprocessError as e:
    logger.warning(f"LibreOffice conversion failed: {e}")
    return None
except FileNotFoundError:  # Use built-in exception
    raise FileNotFoundError(f"File {path} does not exist")
```