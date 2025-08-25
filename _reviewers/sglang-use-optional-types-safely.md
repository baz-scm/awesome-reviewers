---
title: Use Optional types safely
description: Always use proper nullable type annotations and safe access patterns
  to prevent runtime errors from null/undefined values. Use `Optional[Type]` or `Union[None,
  Type]` for nullable parameters, employ safe dictionary access with `.get()`, and
  handle None values explicitly in operations.
repository: sgl-project/sglang
label: Null Handling
language: Python
comments_count: 4
repository_stars: 17245
---

Always use proper nullable type annotations and safe access patterns to prevent runtime errors from null/undefined values. Use `Optional[Type]` or `Union[None, Type]` for nullable parameters, employ safe dictionary access with `.get()`, and handle None values explicitly in operations.

Examples of good practices:
```python
# Use Optional type annotations
def process_data(encoder_lens: Optional[torch.Tensor] = None):
    pass

# Safe dictionary access
draft_url = params.get("draft_url", None)  # Instead of params["draft_url"]

# Null-safe assertions
assert (topk_weights is None) or (topk_weights.shape == topk_ids_.shape)
```

This prevents KeyError exceptions, improves type safety, and makes null handling explicit rather than implicit. Always consider whether a parameter or variable can be None and handle it appropriately in both type annotations and runtime logic.