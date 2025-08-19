---
title: Configuration constants management
description: Extract configuration values into well-named constants instead of using
  magic numbers or inline values. Use consistent naming patterns across environments
  and organize configuration values in a maintainable way.
repository: PostHog/posthog
label: Configurations
language: Python
comments_count: 4
repository_stars: 28460
---

Extract configuration values into well-named constants instead of using magic numbers or inline values. Use consistent naming patterns across environments and organize configuration values in a maintainable way.

**Why this matters:**
- Magic numbers scattered throughout code are hard to maintain and understand
- Inconsistent naming across environments leads to confusion and errors
- Centralized configuration makes it easier to modify behavior without hunting through code

**How to apply:**
1. Replace magic numbers with descriptive constants
2. Use consistent naming patterns across all environments
3. Group related configuration values together
4. Make non-parameterized values into module-level constants

**Example:**
```python
# Bad - magic numbers and inconsistent naming
def paginate_results(self):
    self._page_size = 50
    max_pages = 6
    timeout = 180
    
    if storage_policy == "s3":
        policy = "s3_policy"  # Different naming in other envs

# Good - named constants with consistent patterns
DEFAULT_PAGE_SIZE = 50
MAX_PAGES_LIMIT = 6
REQUEST_TIMEOUT_SECONDS = 180
S3_STORAGE_POLICY = "s3_backed"  # Same across all environments

BASE_ERROR_INSTRUCTIONS = "Tell the user that you encountered an issue..."

def paginate_results(self):
    self._page_size = DEFAULT_PAGE_SIZE
    max_pages = MAX_PAGES_LIMIT
    timeout = REQUEST_TIMEOUT_SECONDS
```

This approach makes configuration changes safer, more discoverable, and reduces the risk of environment-specific bugs.