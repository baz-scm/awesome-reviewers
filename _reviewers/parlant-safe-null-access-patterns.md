---
title: Safe null access patterns
description: Always use safe access patterns to prevent runtime errors when dealing
  with potentially null or undefined values. Instead of direct access that can raise
  KeyError or IndexError, use defensive programming techniques.
repository: emcie-co/parlant
label: Null Handling
language: Python
comments_count: 4
repository_stars: 12205
---

Always use safe access patterns to prevent runtime errors when dealing with potentially null or undefined values. Instead of direct access that can raise KeyError or IndexError, use defensive programming techniques.

For dictionary access, prefer `dict.get(key)` or check `key in dict` before accessing:
```python
# Bad - raises KeyError if key missing
if not os.environ["LITELLM_PROVIDER_MODEL_NAME"]:
    
# Good - safe access patterns  
if "LITELLM_PROVIDER_MODEL_NAME" not in os.environ:
# or
if not os.environ.get("LITELLM_PROVIDER_MODEL_NAME"):
```

For collections, validate bounds before indexing:
```python
# Bad - IndexError if empty
generation = event_generation_result.generations[0]

# Good - check bounds first
if not event_generation_result.generations:
    raise ValueError("No generations available")
generation = event_generation_result.generations[0]
```

Use null coalescing for function parameters:
```python
# Ensure non-null defaults
arguments = tc.arguments or {}
hints = hints or {}  # instead of Optional[dict] = None
```

This prevents common runtime exceptions and makes code more robust when handling optional or potentially missing data.