---
title: Check existence before operations
description: Always verify that keys, IDs, indices, or other required values exist
  before performing operations that depend on them. This prevents runtime errors and
  unexpected behavior from null references or missing data.
repository: PostHog/posthog
label: Null Handling
language: Python
comments_count: 4
repository_stars: 28460
---

Always verify that keys, IDs, indices, or other required values exist before performing operations that depend on them. This prevents runtime errors and unexpected behavior from null references or missing data.

Key patterns to follow:
- Check if dictionary keys exist before registration or access
- Validate that database IDs exist before queries
- Verify array indices are within bounds before access
- Use early returns for cleaner null handling: `if value is None: continue`

Example of the pattern:
```python
# Before: Potential KeyError or duplicate registration
REGISTERED_FUNCTIONS[key] = func

# After: Check existence first
if key in REGISTERED_FUNCTIONS:
    raise ValueError(f"Function {key} already registered")
REGISTERED_FUNCTIONS[key] = func

# Before: Potential IndexError
summary_text_chunk = summary[0]["text"]

# After: Check bounds and existence
if summary and len(summary) > 0:
    summary_text_chunk = summary[0]["text"]
```

This proactive approach prevents silent failures and makes code more robust by catching potential issues at the point of access rather than allowing them to propagate.