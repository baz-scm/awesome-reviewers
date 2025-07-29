---
title: Complete config setting integration
description: When adding new configuration settings, ensure they are properly integrated
  across all required system components. Configuration settings must be registered
  in multiple locations to function correctly and be discoverable by users.
repository: python-poetry/poetry
label: Configurations
language: Python
comments_count: 4
repository_stars: 33496
---

When adding new configuration settings, ensure they are properly integrated across all required system components. Configuration settings must be registered in multiple locations to function correctly and be discoverable by users.

Required integration points include:
- Default values in the main config class
- Normalizer functions for validation/transformation  
- Command-specific config value lists for discoverability
- User-facing documentation and help text

Example of complete integration:
```python
# In Config class defaults
"max-retries": 0,

# In _get_normalizer method  
"max-retries": lambda val: int(val) if val is not None else 0,

# In ConfigCommand.unique_config_values
"max-retries",
```

Additionally, prefer user-facing configuration options over hidden implementation details. When deprecating config keys, use explicit user warnings rather than developer-only deprecation warnings, as these changes directly impact end users.

This systematic approach prevents incomplete configuration implementations that can lead to runtime errors, inconsistent behavior, or poor user experience when settings are partially recognized by the system.