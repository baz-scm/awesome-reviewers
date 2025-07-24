---
title: avoid mutable defaults
description: Never use mutable objects (lists, dictionaries, sets) as default parameter
  values in function definitions. This creates a shared object across all function
  calls, leading to unexpected behavior where modifications persist between calls.
repository: docker/compose
label: Null Handling
language: Python
comments_count: 3
repository_stars: 35858
---

Never use mutable objects (lists, dictionaries, sets) as default parameter values in function definitions. This creates a shared object across all function calls, leading to unexpected behavior where modifications persist between calls.

Instead, use `None` as the default value and assign the mutable object inside the function body. This ensures each function call gets a fresh instance of the mutable object.

**Problem:**
```python
def get_project(project_dir, config_path=None, enabled_profiles=[]):
    # enabled_profiles is shared across all calls!
    enabled_profiles.append("default")
    return enabled_profiles

def project_from_options(project_dir, options, additional_options={}):
    # additional_options is shared across all calls!
    additional_options["key"] = "value"
    return additional_options
```

**Solution:**
```python
def get_project(project_dir, config_path=None, enabled_profiles=None):
    enabled_profiles = enabled_profiles or []
    enabled_profiles.append("default")
    return enabled_profiles

def project_from_options(project_dir, options, additional_options=None):
    additional_options = additional_options or {}
    additional_options["key"] = "value"
    return additional_options
```

This pattern prevents the "least astonishment" principle violation where the same mutable object is reused across function invocations, causing side effects that can be difficult to debug.