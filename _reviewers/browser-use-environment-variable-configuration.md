---
title: Environment variable configuration
description: Prefer environment variables over hardcoded configuration values to improve
  flexibility and avoid forcing configuration choices on users. Always provide sensible
  defaults and implement proper validation.
repository: browser-use/browser-use
label: Configurations
language: Python
comments_count: 5
repository_stars: 69139
---

Prefer environment variables over hardcoded configuration values to improve flexibility and avoid forcing configuration choices on users. Always provide sensible defaults and implement proper validation.

Use environment variables for:
- Feature flags and optional behaviors
- External service endpoints and ports  
- File paths and directory locations
- API keys and authentication tokens

Implementation pattern:
```python
# Good: Environment variable with default and validation
search_engine = os.getenv('BROWSERUSE_SEARCH_ENGINE', 'google').lower().strip()
assert search_engine in ['google', 'bing', 'duckduckgo']

# Good: Configurable port instead of hardcoded
port = int(os.getenv('CHROME_REMOTE_DEBUGGING_PORT', '9222'))
endpoint_url = f'http://localhost:{port}'

# Good: Utility function for env var validation
def check_env_variables(keys: list[str], any_or_all=all) -> bool:
    return any_or_all(os.getenv(key, '').strip() for key in keys)

# Bad: Hardcoded configuration
CAMOUFOX = True  # Should be os.getenv('USE_CAMOUFOX', 'false').lower() == 'true'
```

This approach allows users to customize behavior without code changes while maintaining reasonable defaults for common use cases. Create reusable utility functions for environment variable validation that can be imported across the codebase.