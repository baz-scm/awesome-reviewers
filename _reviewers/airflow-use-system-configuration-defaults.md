---
title: Use system configuration defaults
description: Always use the configuration system's default values instead of hardcoding
  defaults in the code. This ensures consistency across the application and makes
  configuration management more maintainable.
repository: apache/airflow
label: Configurations
language: Python
comments_count: 5
repository_stars: 40858
---

Always use the configuration system's default values instead of hardcoding defaults in the code. This ensures consistency across the application and makes configuration management more maintainable.

Bad:
```python
DEFAULT_QUEUE: str = conf.get("operators", "default_queue", "default")
```

Good:
```python
DEFAULT_QUEUE: str = conf.get_mandatory_value("operators", "default_queue")
```

For provider-specific configurations:
1. Ensure provider configurations are properly loaded using @providers_configuration_loaded decorator
2. Run pre-commits to generate provider configuration files
3. Use conf.get() without fallback when the default is already defined in the configuration system
4. When deprecating configuration options, properly version them in the deprecated_options dictionary

This approach centralizes configuration management, improves maintainability, and ensures consistent behavior across the application.