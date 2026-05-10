---
title: Explicit None Checks
description: When working with nullable/optional values, treat `None` (absence) differently
  from other falsy values like `""` (empty string) or `0` (zero). Use explicit `is
  not None` checks when empty values are valid, and avoid repeating null checks after
  you’ve already established a non-null invariant via an early return/guard.
repository: anthropics/anthropic-sdk-python
label: Null Handling
language: Python
comments_count: 2
repository_stars: 3392
---

When working with nullable/optional values, treat `None` (absence) differently from other falsy values like `""` (empty string) or `0` (zero). Use explicit `is not None` checks when empty values are valid, and avoid repeating null checks after you’ve already established a non-null invariant via an early return/guard.

Apply it like this:
- Prefer `if x is not None:` over `if x:` when `x` may be an empty string/zero but should still be considered “present”.
- After an early return for `None`, don’t add redundant `x is not None` guards later.

Example:
```python
import os

bearer = os.getenv("AWS_BEARER_TOKEN_BEDROCK")
# Empty string is a valid value, so check for None (absence), not truthiness.
if bearer is not None:
    headers["Authorization"] = f"Bearer {bearer}"

# Later, avoid redundant None checks after a guard/early return:
if response is None:
    return
if response.get("content"):
    append_messages(message, response)
```