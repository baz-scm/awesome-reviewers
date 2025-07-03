---
title: Handle non-deterministic collections
description: When working with hash-based collections like sets or dictionaries, be
  aware that their ordering is non-deterministic across Python interpreter runs. This
  can cause subtle bugs in algorithms that rely on consistent ordering.
repository: pytorch/pytorch
label: Algorithms
language: Python
comments_count: 5
repository_stars: 91169
---

When working with hash-based collections like sets or dictionaries, be aware that their ordering is non-deterministic across Python interpreter runs. This can cause subtle bugs in algorithms that rely on consistent ordering.

For example, accessing set elements by position can yield different results between runs:

```python
# Inconsistent across Python runs!
s = set("abc")
list(s)[0]  # Could be 'a', 'b', or 'c' depending on hash randomization
```

Instead:
1. For sets, if you need consistent ordering, convert to a sorted list:
```python
sorted_items = sorted(my_set)  # Now has deterministic ordering
```

2. When implementing algorithms that access collections by index, document non-determinism:
```python
def set_getitem(s, n):
    # Note: Returns the nth item in arbitrary order
    # Recompilation may occur if hash order changes
    return list(s)[n]
```

3. For code that might be traced/compiled (e.g., with PyTorch Dynamo), prefer operations that don't depend on ordering, and be explicit when you do:
```python
# Prefer operations like:
if x in my_set:  # Order-independent
    ...

# Instead of:
first_element = next(iter(my_set))  # Order-dependent!
```

Remember that hash values for strings and other objects vary across interpreter runs due to Python's hash randomization security feature. Always ensure algorithms that interact with hash-based collections handle this non-determinism appropriately.
