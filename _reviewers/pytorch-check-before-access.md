---
title: Check before access
description: Always check for null/None values and verify attribute/key existence
  before accessing them. This prevents runtime errors like AttributeError or KeyError
  that occur when accessing attributes on None or missing dictionary keys.
repository: pytorch/pytorch
label: Null Handling
language: Python
comments_count: 7
repository_stars: 91169
---

Always check for null/None values and verify attribute/key existence before accessing them. This prevents runtime errors like AttributeError or KeyError that occur when accessing attributes on None or missing dictionary keys.

When accessing attributes:
```python
# Bad: May cause AttributeError if current_accelerator() returns None
device_type = torch.accelerator.current_accelerator().type

# Good: Check before access
accelerator = torch.accelerator.current_accelerator()
if accelerator is not None:
    device_type = accelerator.type
else:
    device_type = "cpu"  # Default fallback

# Bad: May cause AttributeError if func doesn't have tags attribute
if torch.Tag.inplace_view in func.tags:
    # ...

# Good: Check attribute existence first
if hasattr(func, "tags") and torch.Tag.inplace_view in func.tags:
    # ...
```

When accessing dictionary keys:
```python
# Bad: May raise KeyError if key doesn't exist
lst.append(f'* {obj["DeviceName"]}')

# Good: Use .get() with a default value
lst.append(f'* {obj.get("DeviceName", "N/A")}')

# Bad: May fail if device_list is missing or not a list
if type(obj["device_list"]) is list:
    # ...

# Good: Check existence and type safely
device_list = obj.get("device_list", [])
if isinstance(device_list, list) and device_list:
    # ...
```

When checking types:
```python
# Bad: May fail if storage_writer is None
if isinstance(storage_writer, AsyncStager):
    # ...

# Good: Check for None first
if storage_writer is not None and isinstance(storage_writer, AsyncStager):
    # ...
```

This defensive programming approach reduces unexpected crashes and improves code robustness.
