---
title: validate before processing
description: Always validate input state and types before performing operations to
  prevent runtime errors and unexpected behavior. This includes checking data types
  before applying type-specific operations and preserving object state when performing
  validation checks.
repository: microsoft/markitdown
label: Null Handling
language: Python
comments_count: 2
repository_stars: 76602
---

Always validate input state and types before performing operations to prevent runtime errors and unexpected behavior. This includes checking data types before applying type-specific operations and preserving object state when performing validation checks.

When working with streams, restore the original position after reading during validation to avoid side effects:

```python
# Good: Preserve stream position
cur_pos = file_stream.tell()
data = file_stream.read()
file_stream.seek(cur_pos)
```

When processing data, validate the type before applying operations:

```python
# Good: Check type before text operations
if isinstance(content, str):
    content = self._strip_leading_blanks(content)
```

This defensive approach prevents errors from assumptions about input state or type, similar to how null checks prevent null reference exceptions.