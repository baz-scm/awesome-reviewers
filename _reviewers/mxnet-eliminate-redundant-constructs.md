---
title: Eliminate redundant constructs
description: 'Remove unnecessary coding patterns that add complexity without providing
  value. Focus on clarity and simplicity by:


  1. Not using enumerate() when the index is unused:'
repository: apache/mxnet
label: Code Style
language: Python
comments_count: 12
repository_stars: 20801
---

Remove unnecessary coding patterns that add complexity without providing value. Focus on clarity and simplicity by:

1. Not using enumerate() when the index is unused:
```python
# Instead of:
for _, item in enumerate(collection):
    process(item)
    
# Use:
for item in collection:
    process(item)
```

2. Using generator expressions instead of list comprehensions when creating iterables directly:
```python
# Instead of:
return tuple([x.astype(dtype) for x in args])

# Use:
return tuple(x.astype(dtype) for x in args)
```

3. Following Python's idiomatic expressions for boolean operations:
```python
# Instead of:
if (upper == False):
    do_something()
    
# Use:
if not upper:
    do_something()
```

These simplifications improve code readability and maintain a clean, Pythonic style that aligns with best practices.
