---
title: safe environment variable access
description: Always use `os.environ.get()` with appropriate defaults instead of direct
  dictionary access to prevent KeyError exceptions when environment variables are
  not set. Additionally, extract configuration constants and magic numbers to named
  module-level variables for better maintainability and consistency.
repository: emcie-co/parlant
label: Configurations
language: Python
comments_count: 4
repository_stars: 12205
---

Always use `os.environ.get()` with appropriate defaults instead of direct dictionary access to prevent KeyError exceptions when environment variables are not set. Additionally, extract configuration constants and magic numbers to named module-level variables for better maintainability and consistency.

This pattern prevents runtime crashes when optional environment variables are missing and makes configuration values more discoverable and maintainable.

**Problematic pattern:**
```python
api_version = os.environ["AZURE_API_VERSION"] or "2024-08-01-preview"  # KeyError if not set
await asyncio.sleep(10)  # Magic number
```

**Preferred pattern:**
```python
# Module-level constants
DEFAULT_API_VERSION = "2024-08-01-preview"
EXTENDED_PERIOD_OF_TIME = 10

# Safe environment variable access
api_version = os.environ.get("AZURE_API_VERSION", DEFAULT_API_VERSION)
await asyncio.sleep(EXTENDED_PERIOD_OF_TIME)
```

This approach ensures graceful handling of missing environment variables while making configuration values explicit and easily adjustable across the codebase.