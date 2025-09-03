---
title: Use configuration helper utilities
description: Always use centralized helper functions for configuration management
  instead of direct environment variable access or hardcoded values. This ensures
  consistency, maintainability, and proper error handling across the codebase.
repository: BerriAI/litellm
label: Configurations
language: Python
comments_count: 5
repository_stars: 28310
---

Always use centralized helper functions for configuration management instead of direct environment variable access or hardcoded values. This ensures consistency, maintainability, and proper error handling across the codebase.

Key practices:
- Use `get_secret_str()` utility for sensitive configuration values instead of `os.environ.get()`
- Use `str_to_bool()` for boolean environment variables instead of manual string comparison
- Create helper functions in common utilities (e.g., `llms/gemini/common_utils.py`) for provider-specific configuration logic
- Move hardcoded constants to `constants.py` and control them through environment variables

Example of proper configuration handling:
```python
# Bad - direct environment access and hardcoded values
api_key = os.environ.get("GEMINI_API_KEY")
MAX_STRING_LENGTH = 1000
if os.getenv("NO_REDOC", "False") == "True":

# Good - using helper utilities
api_key = get_secret_str("GEMINI_API_KEY") or get_secret_str("GOOGLE_API_KEY")
MAX_STRING_LENGTH = get_secret_str("MAX_STRING_LENGTH_PROMPT_IN_DB", "1000")
if str_to_bool(os.getenv("NO_REDOC", "False")):
```

This approach prevents configuration drift, reduces code duplication, and makes configuration behavior predictable across different parts of the system.