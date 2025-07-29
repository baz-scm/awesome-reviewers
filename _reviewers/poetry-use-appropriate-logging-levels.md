---
title: Use appropriate logging levels
description: Use debug-level logging for technical details and error information that
  aids developer troubleshooting, while keeping user-facing messages clean and informative.
  Avoid exposing verbose technical details directly to users, but ensure they are
  available for debugging.
repository: python-poetry/poetry
label: Logging
language: Python
comments_count: 4
repository_stars: 33496
---

Use debug-level logging for technical details and error information that aids developer troubleshooting, while keeping user-facing messages clean and informative. Avoid exposing verbose technical details directly to users, but ensure they are available for debugging.

Technical error details, exception information, and diagnostic data should be logged at debug level to help developers troubleshoot issues without overwhelming end users. User-facing messages should remain concise and actionable.

Example:
```python
try:
    SystemGit.clone(url, target)
except CalledProcessError as e:
    logger.debug("Git command returned the following error:\n%s", e.stderr)
    raise PoetryConsoleError(
        f"Failed to clone {url}, check your git configuration and permissions"
        " for this repository."
    )
```

Also add debug logging for edge cases and error conditions that might not be immediately obvious:
```python
def get_highest_priority_hash_type(hash_types: set[str]) -> str | None:
    if not hash_types:
        return None
    
    for prioritised_hash_type in prioritised_hash_types:
        if prioritised_hash_type in hash_types:
            return prioritised_hash_type
    
    logger.debug('None of the hash types %s is in prioritized_hash_types', hash_types)
    # ... handle fallback cases
```