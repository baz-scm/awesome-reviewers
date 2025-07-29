---
title: Explicit null handling
description: Use explicit and clear patterns when handling null/None values to improve
  code readability and maintainability. Avoid complex conditional expressions, unnecessary
  type casting, and ambiguous nullable types.
repository: python-poetry/poetry
label: Null Handling
language: Python
comments_count: 8
repository_stars: 33496
---

Use explicit and clear patterns when handling null/None values to improve code readability and maintainability. Avoid complex conditional expressions, unnecessary type casting, and ambiguous nullable types.

**Key principles:**

1. **Prefer explicit None checks over complex expressions:**
```python
# Prefer this
if version is None:
    version = packages[0] if packages else None

# Over this  
version = version or packages[0]
```

2. **Use None to mean "unknown" and empty collections for "known empty":**
```python
# Use None when data availability is uncertain
requires_dist = None  # "I don't know what the requirements are"

# Use empty list when you know there are no requirements  
requires_dist = []  # "I know there are no requirements"
```

3. **Use safe access patterns with appropriate defaults:**
```python
# Safe dictionary access
name = poetry.local_config.get("name", "")
headers = kwargs.get("headers", {}) or {}

# Safe attribute checking
if "name" in distribution.metadata:
    name = distribution.metadata["name"]
```

4. **Avoid unnecessary nullable types:**
```python
# Don't make parameters nullable if they're never actually None
def configure_options(self, io: IO) -> None:  # Not IO | None
    # io is always provided by caller
```

5. **Check None conditions first when it's the default case:**
```python
# Put the default/expected case first
if output is None:
    sys.stdout.write(content)
else:
    with open(output, 'w') as f:
        f.write(content)
```

6. **Prefer direct None checks over type casting:**
```python
# Prefer this
if self._cache_control is None:
    return None

# Over this with cast
if self._disable_cache:
    return None
# ... later: cast(CacheControl, self._cache_control)
```

These patterns make null handling intentions clear, reduce the risk of runtime errors, and improve code maintainability by making the expected behavior explicit.