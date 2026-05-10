---
title: Preserve Null Semantics
description: 'When inputs or response fields are optional/nullable, preserve their
  semantics explicitly and avoid unsafe coercion or indexing.


  Apply these rules:

  1) Don’t coerce `None` with `bool(...)` when `None` has distinct meaning. If you
  mean “unset,” omit the field/parameter rather than converting it.'
repository: openai/openai-python
label: Null Handling
language: Python
comments_count: 4
repository_stars: 30731
---

When inputs or response fields are optional/nullable, preserve their semantics explicitly and avoid unsafe coercion or indexing.

Apply these rules:
1) Don’t coerce `None` with `bool(...)` when `None` has distinct meaning. If you mean “unset,” omit the field/parameter rather than converting it.
2) Don’t blindly index into dicts/JSON (`obj["key"]`) when keys may be missing; use `obj.get("key", default)` (often `{}`) to prevent exceptions.
3) When building request artifacts (e.g., headers), only include values when the input is actually present; otherwise, send an empty structure or omit the header.

Example patterns:
```python
# 1) Tri-state optional: None => omit
payload = {}
if by_alias is not None:
    payload["by_alias"] = by_alias  # preserve None-vs-explicit

# 2) Safe dict access
error_data = response.data.get("error", {})
message = error_data.get("message", "Operation failed")

# 3) Conditional auth header
headers = {} if not api_key else {"Authorization": f"Bearer {api_key}"}
```

Result: fewer runtime KeyErrors/invalid requests, and correct behavior when upstream defaults/configuration rely on “unset” vs “explicit value.”