---
title: Centralize error handling
description: Consolidate error handling logic into central, unavoidable locations
  rather than scattering it across multiple functions or requiring manual setup. This
  prevents cases where error handling can be bypassed or forgotten.
repository: cloudflare/workerd
label: Error Handling
language: Python
comments_count: 3
repository_stars: 6989
---

Consolidate error handling logic into central, unavoidable locations rather than scattering it across multiple functions or requiring manual setup. This prevents cases where error handling can be bypassed or forgotten.

When you have error handling setup, exception conversion, or similar logic that must always execute, place it in functions that are guaranteed to be called rather than relying on developers to remember to call constructors or helper functions.

For example, instead of requiring users to call a constructor that sets up error handling:
```python
def __init__(self, ctx, env):
    _pyodide_entrypoint_helper.patchWaitUntil(ctx)  # Can be missed if super() not called
```

Move the setup to a central function that cannot be bypassed:
```python
# In doPyCallHelper() - always called, impossible to miss
_pyodide_entrypoint_helper.patchWaitUntil(ctx)
```

Similarly, consolidate exception conversion logic into existing central functions like `_to_python_exception()` rather than creating separate functions that handle overlapping cases. This ensures consistent error handling and reduces the chance of missing edge cases.