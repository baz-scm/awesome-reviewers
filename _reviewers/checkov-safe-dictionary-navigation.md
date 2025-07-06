---
title: Safe dictionary navigation
description: Always use the `.get()` method with appropriate default values when accessing
  dictionaries instead of direct key access with brackets. This prevents KeyError
  exceptions when keys don't exist and provides predictable default values. For nested
  dictionaries, chain `.get()` calls with empty dictionaries as defaults for intermediate
  levels.
repository: bridgecrewio/checkov
label: Null Handling
language: Python
comments_count: 9
repository_stars: 7668
---

Always use the `.get()` method with appropriate default values when accessing dictionaries instead of direct key access with brackets. This prevents KeyError exceptions when keys don't exist and provides predictable default values. For nested dictionaries, chain `.get()` calls with empty dictionaries as defaults for intermediate levels.

Example of problematic code:
```python
# May raise KeyError if 'properties' or 'siteConfig' keys don't exist
if conf['properties']['siteConfig'] is not None:
    # process configuration
```

Improved version:
```python
# Safely handles missing keys with default values
if conf.get('properties', {}).get('siteConfig') is not None:
    # process configuration
```

For collections that should be lists, provide an empty list as the default:
```python
# Safe access for list-type values
for item in conf.get('items', []):
    # process each item
```

When type checking is necessary before access:
```python
# Verify both existence and type
if conf.get('properties') and isinstance(conf.get('properties'), dict):
    # safely work with the dictionary value
```

Always verify that a value is the expected type before accessing its attributes or performing operations, especially after retrieving it with `.get()`.