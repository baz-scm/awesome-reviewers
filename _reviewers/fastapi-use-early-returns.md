---
title: Use early returns
description: Decrease indentation levels in your code by using early returns for edge
  cases and guard conditions. This approach improves readability by reducing nesting
  and making the code flow more linear.
repository: fastapi/fastapi
label: Code Style
language: Python
comments_count: 4
repository_stars: 86871
---

Decrease indentation levels in your code by using early returns for edge cases and guard conditions. This approach improves readability by reducing nesting and making the code flow more linear.

Instead of wrapping your main logic in conditional blocks:

```python
def process_data(data):
    if data is not None:
        # Process data here (indented)
        result = transform(data)
        return result
    else:
        return None
        
# In loops:
for param in parameters:
    if field_info.include_in_schema:
        # Process parameter (indented)
        # Many lines of code
```

Prefer checking conditions that allow early exit, then handle the main logic with less indentation:

```python
def process_data(data):
    if data is None:
        return None
    # Process data here (not indented)
    result = transform(data)
    return result
    
# In loops:
for param in parameters:
    if not field_info.include_in_schema:
        continue
    # Process parameter (not indented)
    # Many lines of code
```

Similarly, avoid unnecessary else blocks after returns, and use early continues in loops to keep your code flat and easier to follow.