---
title: Centralize environment variables
description: All environment variables should be defined in a centralized location
  (`checkov/common/util/env_vars_config.py`) rather than scattered throughout the
  codebase. This approach enhances maintainability, promotes consistency, and simplifies
  tracking of configuration settings.
repository: bridgecrewio/checkov
label: Configurations
language: Python
comments_count: 9
repository_stars: 7668
---

All environment variables should be defined in a centralized location (`checkov/common/util/env_vars_config.py`) rather than scattered throughout the codebase. This approach enhances maintainability, promotes consistency, and simplifies tracking of configuration settings.

When adding a new environment variable:
1. Define it in the centralized config file with proper type conversion
2. Add a descriptive comment explaining its purpose
3. Import and use the variable in your code instead of direct `os.getenv()` calls

Always use `strtobool()` for boolean environment variables since `bool('False')` evaluates to `True`.

Example:
```python
# In checkov/common/util/env_vars_config.py
from distutils.util import strtobool

# Controls whether to ignore hidden directories (default: True)
IGNORE_HIDDEN_DIRECTORY_ENV = strtobool(os.getenv("CKV_IGNORE_HIDDEN_DIRECTORIES", "True"))

# In your code
from checkov.common.util.env_vars_config import IGNORE_HIDDEN_DIRECTORY_ENV

if IGNORE_HIDDEN_DIRECTORY_ENV:
    # Skip hidden directories logic here
```