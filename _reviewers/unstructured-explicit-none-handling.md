---
title: explicit None handling
description: Always handle potential None values explicitly through defensive programming
  patterns, proper type annotations, and explicit checks to prevent runtime errors
  and improve code reliability.
repository: Unstructured-IO/unstructured
label: Null Handling
language: Python
comments_count: 11
repository_stars: 12116
---

Always handle potential None values explicitly through defensive programming patterns, proper type annotations, and explicit checks to prevent runtime errors and improve code reliability.

Use defensive patterns like `value or default` for safe fallbacks:
```python
# Good: Explicit None handling with fallback
e.metadata.languages = detect_languages(e.text or "")
full_text = " ".join(e.text or "" for e in elements if hasattr(e, "text"))

# Good: Explicit None checks with proper logic
if encoding is None or (confidence is not None and confidence < ENCODE_REC_THRESHOLD):
    # handle the case
```

Use proper Optional type annotations when values can be None:
```python
# Good: Correct Optional typing
max_pages: Optional[int] = None
customer_id: Optional[str] = None

# Bad: Missing Optional annotation
customer_id: str = None  # Type mismatch
```

Handle functions that may return None explicitly:
```python
# Good: Check for None return value
nltk_data_dir = get_nltk_data_dir()
if nltk_data_dir is None:
    raise ValueError("Could not find a default download directory")

# Good: Use assertions when None is guaranteed not to occur
assert self._file is not None  # -- assured by ._validate() --
```

Avoid unnecessary None-to-string conversions and prefer removing optionality at interface boundaries when the None case adds no value. When designing APIs, consider whether Optional parameters truly need to be optional or if a sensible default can be provided instead.