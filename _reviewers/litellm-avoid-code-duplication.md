---
title: Avoid code duplication
description: Eliminate redundant code by leveraging existing utilities, extracting
  reusable helper functions, and organizing logic in appropriate modules. Before implementing
  new functionality, check if similar logic already exists in the codebase that can
  be reused or extended.
repository: BerriAI/litellm
label: Code Style
language: Python
comments_count: 15
repository_stars: 28310
---

Eliminate redundant code by leveraging existing utilities, extracting reusable helper functions, and organizing logic in appropriate modules. Before implementing new functionality, check if similar logic already exists in the codebase that can be reused or extended.

Key practices:
- Use existing utilities instead of reimplementing logic (e.g., use `get_deployment` in router.py rather than duplicating deployment lookup logic)
- Extract common logic into helper functions or static methods to avoid repetition across multiple locations
- Organize provider-specific logic in dedicated transformation files rather than mixing it in generic handlers
- Move utility functions to appropriate modules (e.g., proxy/utils.py) rather than defining them inline
- Create reusable helper utilities for common patterns that can be shared across endpoints

Example of refactoring duplicate logic:
```python
# Before: Duplicate SSL verification logic
ssl_verify = (os.getenv("SSL_VERIFY") != "False") if os.getenv("SSL_VERIFY") is not None else litellm.ssl_verify

# After: Extract to helper method
def get_ssl_verify_setting():
    return (os.getenv("SSL_VERIFY") != "False") if os.getenv("SSL_VERIFY") is not None else litellm.ssl_verify

ssl_verify = get_ssl_verify_setting()
```

This approach reduces maintenance burden, improves consistency, and makes the codebase more maintainable by centralizing common logic.