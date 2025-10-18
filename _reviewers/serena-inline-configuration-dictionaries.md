---
title: Inline configuration dictionaries
description: Avoid storing simple configuration data in separate JSON files. Instead,
  define configuration as Python dictionaries directly within the relevant modules.
  This approach reduces file overhead, improves maintainability, and keeps related
  code together.
repository: oraios/serena
label: Configurations
language: Json
comments_count: 2
repository_stars: 14465
---

Avoid storing simple configuration data in separate JSON files. Instead, define configuration as Python dictionaries directly within the relevant modules. This approach reduces file overhead, improves maintainability, and keeps related code together.

When configuration is static and doesn't require external modification, inline dictionaries are preferred over separate JSON files. This pattern should be used for initialization parameters, default settings, and other module-specific configuration data.

Example transformation:
```python
# Instead of loading from initialize_params.json
# with open('initialize_params.json') as f:
#     config = json.load(f)

# Define configuration directly in the module
INITIALIZE_PARAMS = {
    "processId": None,
    "clientInfo": {
        "name": "solidlsp",
        "version": "1.0.0"
    },
    "capabilities": {
        "textDocument": {
            "completion": {"completionItem": {"snippetSupport": True}}
        }
    }
}
```

Reserve external JSON files for configuration that needs to be modified by users or varies between environments.