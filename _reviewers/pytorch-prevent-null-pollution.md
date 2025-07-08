---
title: Prevent null pollution
description: Design your code to minimize the unexpected introduction of None values
  into data structures and APIs. Use immutable parameter types when you don't need
  to modify the input, and be explicit about nullable types to establish clear contracts.
repository: pytorch/pytorch
label: Null Handling
language: Python
comments_count: 5
repository_stars: 91345
---

Design your code to minimize the unexpected introduction of None values into data structures and APIs. Use immutable parameter types when you don't need to modify the input, and be explicit about nullable types to establish clear contracts.

```python
# Bad: Unexpectedly modifies input with None values
def process_data(progression_futures: list):
    progression_futures.append(None)  # Caller now has List[Optional[...]]
    
# Good: Communicates intent with immutable parameter type
def process_data(progression_futures: Sequence):
    # Create a new collection instead of modifying input
    result = list(progression_futures) + [None]
    return result

# Good: Be explicit about nullable return values
def get_first(items: list[Optional[str]]) -> Optional[str]:
    return items[0] if items else None
```

When handling potentially null attributes or dictionary keys, use concise safe access patterns:

```python
# Verbose and error-prone
if "max_version" in kwargs:
    kwargs.pop("max_version")

# Better: Use safe dictionary operations
kwargs.pop("max_version", None)  # No KeyError if missing

# Verbose attribute access
name = str(e.name) if hasattr(e, 'name') else str(e)

# Better: Use getattr with default
name = str(getattr(e, "name", e))
```