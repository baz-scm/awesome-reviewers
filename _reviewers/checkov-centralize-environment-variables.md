---
title: Centralize environment variables
description: All environment variables should be defined in a central configuration
  file and imported where needed, rather than scattered throughout the codebase. This
  practice improves maintainability, ensures consistency, and makes configuration
  management more robust.
repository: bridgecrewio/checkov
label: Configurations
language: Python
comments_count: 7
repository_stars: 7667
---

All environment variables should be defined in a central configuration file and imported where needed, rather than scattered throughout the codebase. This practice improves maintainability, ensures consistency, and makes configuration management more robust.

Key practices to follow:
1. Define all environment variables in `checkov/common/util/env_vars_config.py`
2. Use proper type conversion functions for environment variables
3. Import environment variables from the central file instead of directly accessing them with `os.getenv()`

Example:
```python
# INCORRECT - Defining environment variables locally in different files
def some_function():
    use_feature = bool(os.getenv('FEATURE_FLAG', 'False'))  # Also incorrect conversion!
    if use_feature:
        # Feature-specific code

# CORRECT - Define in central config file (env_vars_config.py)
FEATURE_FLAG = strtobool(os.getenv('FEATURE_FLAG', 'False'))

# Then import and use in other files
from checkov.common.util.env_vars_config import FEATURE_FLAG

def some_function():
    if FEATURE_FLAG:
        # Feature-specific code
```

Note that when converting string environment variables to boolean values, use `strtobool()` instead of `bool()`, as `bool('False')` evaluates to `True`.