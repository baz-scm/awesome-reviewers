---
title: Use proper logging practices
description: Always use logging instead of print statements, and choose appropriate
  log levels to avoid log spam. Print statements can contaminate the stdio buffer
  and break system functionality, especially in server environments.
repository: oraios/serena
label: Logging
language: Python
comments_count: 4
repository_stars: 14465
---

Always use logging instead of print statements, and choose appropriate log levels to avoid log spam. Print statements can contaminate the stdio buffer and break system functionality, especially in server environments.

Use logging with appropriate levels:
- `logger.warning()` for recoverable issues that need attention (e.g., encoding fallbacks)
- `logger.debug()` for detailed information that might be verbose
- Consolidate repetitive logs to avoid spam

Example of proper logging practices:

```python
# Bad - using print statements
print("DEBUG: Starting terraform version detection...")
print(f"Elixir test repository already compiled in {repo_path}")

# Good - using appropriate logging levels
logger.debug("Starting terraform version detection...")
logger.info(f"Elixir test repository already compiled in {repo_path}")

# Good - warning for fallback scenarios
logger.warning(f"Could not decode {file_path} with encoding='{encoding}'; using best match '{match.encoding}' instead")

# Good - debug level for potentially verbose information
logger.debug(f"Skipping {path}: does not match include pattern {paths_include_glob}")
```

This prevents stdio buffer contamination and ensures logs are properly categorized and filterable.