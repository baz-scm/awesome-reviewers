---
title: Safe access patterns
description: Always use safe access methods when working with potentially null or
  undefined values. Use .get() for dictionary access, check array bounds before indexing,
  and validate existence before operations.
repository: BerriAI/litellm
label: Null Handling
language: Python
comments_count: 9
repository_stars: 28310
---

Always use safe access methods when working with potentially null or undefined values. Use .get() for dictionary access, check array bounds before indexing, and validate existence before operations.

Key patterns to follow:
- Use `dict.get("key")` instead of `dict["key"]` for optional fields
- Check `len(array) > 0` before accessing `array[0]`
- Use `if value is not None:` for explicit null checks
- Avoid using `or` operator for fallback values when 0 or empty strings are valid (use explicit None checks instead)

Example of safe patterns:
```python
# Safe dictionary access
description = tool.get("description")  # Instead of tool["description"]
api_key = deployment.get("litellm_params", {}).get("api_key")

# Safe array access  
if len(results) > 0 and results[0].get("moderations"):
    # Process moderations

# Proper null checking logic
if all([batch_cost is not None, batch_usage is not None, batch_models is not None]):
    # Process batch data

# Safe fallback with explicit None check
_deployment_tpm = _deployment.get("tpm")
if _deployment_tpm is None:
    _deployment_tpm = _deployment.get("litellm_params", {}).get("tpm")
if _deployment_tpm is None:
    _deployment_tpm = float("inf")
```

This prevents KeyError exceptions, IndexError exceptions, and unexpected behavior from falsy values being treated as None.