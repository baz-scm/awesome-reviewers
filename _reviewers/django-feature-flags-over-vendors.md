---
title: Feature flags over vendors
description: When checking for database backend capabilities, always use feature flags
  rather than checking specific vendor names. This makes your code more maintainable
  and vendor-agnostic while allowing third-party backends to implement support through
  the feature flag system.
repository: django/django
label: Configurations
language: Python
comments_count: 3
repository_stars: 84182
---

When checking for database backend capabilities, always use feature flags rather than checking specific vendor names. This makes your code more maintainable and vendor-agnostic while allowing third-party backends to implement support through the feature flag system.

Instead of explicitly checking the vendor:

```python
if connection.vendor == "sqlite":
    # SQLite-specific implementation
    ...
else:
    # Implementation for other databases
    ...
```

Declare and use feature flags:

```python
# In database feature definition
class DatabaseFeatures:
    supports_json_absent_on_null = property(lambda self: self.connection.vendor != "sqlite")

# In your code
if connection.features.supports_json_absent_on_null:
    # Use feature requiring JSON ABSENT ON NULL
    ...
else:
    # Use alternative implementation or raise NotSupportedError
    raise NotSupportedError("This database does not support ABSENT ON NULL")
```

This pattern centralizes capability detection in feature flags rather than spreading vendor-specific checks throughout the codebase, making it easier to update support for features across different database backends.