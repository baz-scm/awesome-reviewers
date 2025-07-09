---
title: Validate configurations up front
description: Always validate configuration parameters and environment variables at
  initialization time, providing clear error messages for missing or invalid values.
  This helps catch configuration issues early and makes debugging easier.
repository: crewaiinc/crewai
label: Configurations
language: Python
comments_count: 3
repository_stars: 33945
---

Always validate configuration parameters and environment variables at initialization time, providing clear error messages for missing or invalid values. This helps catch configuration issues early and makes debugging easier.

Key practices:
1. Check required environment variables before attempting to use associated features
2. Validate configuration parameters at initialization
3. Provide clear, actionable error messages
4. Respect configuration hierarchy (passed parameters take precedence over environment variables)

Example:
```python
def __init__(self, api_key: Optional[str] = None):
    # Check required env vars early
    if not api_key and "REQUIRED_API_KEY" not in os.environ:
        raise ValueError(
            "API key must be provided either through initialization parameter "
            "or REQUIRED_API_KEY environment variable"
        )
    
    # Respect parameter hierarchy
    self.api_key = api_key or os.environ["REQUIRED_API_KEY"]
    
    # Only import optional dependencies if configured
    if self.api_key:
        try:
            from optional_package import OptionalClient
            self.client = OptionalClient(self.api_key)
        except ImportError:
            raise ImportError(
                "Optional package is required when using this feature. "
                "Install it with: pip install optional_package"
            )
```