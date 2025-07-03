---
title: Validate environment variables
description: Environment variables are a common source of configuration in Python
  code, but they require proper handling to avoid subtle bugs. Always normalize and
  validate environment variables when they are read, and use appropriate helper functions
  for type conversion.
repository: pytorch/pytorch
label: Configurations
language: Python
comments_count: 5
repository_stars: 91169
---

Environment variables are a common source of configuration in Python code, but they require proper handling to avoid subtle bugs. Always normalize and validate environment variables when they are read, and use appropriate helper functions for type conversion.

Key practices:
1. **Normalize values** by stripping whitespace and considering case-sensitivity:
```python
# Good - normalize for consistent comparison
value = os.environ.get('MY_CONFIG_FLAG')
if value:
    value = value.strip().lower()
```

2. **Use helper functions** for boolean values instead of direct conversion:
```python
# Bad - semantically broken
if bool(os.getenv("USE_SYSTEM_LIBS", False)):

# Good - handles "false", "0", etc. correctly
def str2bool(val):
    return val.lower() in ("yes", "true", "t", "1")
    
if str2bool(os.getenv("USE_SYSTEM_LIBS", "false")):
```

3. **Follow standard specifications** for configuration paths:
```python
# Bad - doesn't respect XDG specification
cache_dir = os.path.expanduser("~/.cache/")

# Good - respects XDG specification
cache_dir = os.getenv("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))
```

4. **Read environment variables close to usage** instead of defining them globally:
```python
# Bad - defined far from usage
CKPT_PIN_ALLOW_RETRY = os.environ.get("CKPT_PIN_ALLOW_RETRY", "1") == "1"
# ... many lines later ...
if CKPT_PIN_ALLOW_RETRY:
    # use flag

# Good - defined close to usage
if os.environ.get("CKPT_PIN_ALLOW_RETRY", "1") == "1":
    # use flag
```

5. **Use early returns** to simplify platform-specific logic:
```python
# Bad
if get_platform() == "linux":
    # linux-specific code
    return result
return "N/A"

# Good
if get_platform() != "linux":
    return "N/A"
# linux-specific code
return result
```

Properly handling environment variables improves code reliability, maintainability, and makes behavior more predictable across different environments.
