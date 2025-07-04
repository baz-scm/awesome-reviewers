---
title: Structured configuration management
description: Configuration files should follow official standards, have up-to-date
  tool settings, and appropriate dependency constraints. This ensures consistent behavior
  across environments and compatibility with the project's requirements.
repository: pydantic/pydantic
label: Configurations
language: Toml
comments_count: 3
repository_stars: 24377
---

Configuration files should follow official standards, have up-to-date tool settings, and appropriate dependency constraints. This ensures consistent behavior across environments and compatibility with the project's requirements.

For pyproject.toml:
1. Organize sections according to packaging specifications (e.g., place dependency-groups under the project section)
2. Keep tool configuration versions aligned with project requirements:
   ```toml
   [tool.ruff]
   target-version = 'py39'  # Should match minimum supported Python version
   ```
3. Manage dependency constraints carefully, considering Python version compatibility:
   ```toml
   # Option 1: Version constraints with conditions
   "sqlalchemy>=2.0,<3.0; python_version < '3.13'"
   
   # Option 2: Simpler constraints when appropriate
   "sqlalchemy>=2.0,<3.0"
   ```

Regular audits of configuration files should be performed when upgrading dependencies or changing supported Python versions to ensure configurations remain correct and optimal.