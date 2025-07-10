---
title: Use connection by alias
description: When working with database operations in Django projects that might use
  multiple database backends, always access database features and operations through
  `connections[alias]` instead of the global `connection` object. This ensures your
  code works correctly regardless of which database backend is being used for a specific
  operation.
repository: django/django
label: Database
language: Python
comments_count: 6
repository_stars: 84182
---

When working with database operations in Django projects that might use multiple database backends, always access database features and operations through `connections[alias]` instead of the global `connection` object. This ensures your code works correctly regardless of which database backend is being used for a specific operation.

For example, instead of:

```python
def db_returning(self):
    """Private API intended only to be used by Django itself."""
    return (
        self.has_db_default() and connection.features.can_return_columns_from_insert
    )
```

Use:

```python
def db_returning(self):
    """Private API intended only to be used by Django itself."""
    return self.has_db_default()
```

And check the feature at the appropriate time with the correct connection:
```python
if connections[using].features.can_return_columns_from_insert:
    # Perform operation with RETURNING clause
```

This approach prevents bugs in multi-database setups where features vary across backends, such as when the default database is MySQL but you're also using PostgreSQL for specific operations.