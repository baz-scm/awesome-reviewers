---
title: Defensive null value handling
description: 'Always handle potential null/None values defensively by:

  1. Using `.get()` for dictionary access instead of direct key access

  2. Checking for None/falsy values before accessing their properties'
repository: boto/boto3
label: Null Handling
language: Python
comments_count: 7
repository_stars: 9417
---

Always handle potential null/None values defensively by:
1. Using `.get()` for dictionary access instead of direct key access
2. Checking for None/falsy values before accessing their properties
3. Initializing None defaults explicitly rather than using mutable defaults

Example:
```python
# Bad:
def process_response(response):
    items = response['items']  # May raise KeyError
    return items['data']  # Nested access compounds risk

# Good:
def process_response(response, extra_params=None):
    if extra_params is None:
        extra_params = {}
    
    items = response.get('items')
    if not items:  # Handles None and empty dict
        return None
    
    return items.get('data')  # Safe nested access
```

This pattern:
- Prevents KeyError exceptions from missing dictionary keys
- Avoids NoneType attribute errors
- Maintains consistent return types
- Makes null cases explicit and intentional
- Improves code robustness and maintainability