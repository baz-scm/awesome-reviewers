---
title: Null-Safe Input Normalization
description: 'Always treat nullable/optional fields and parsed payloads as untrusted
  at boundaries: normalize `None`/missing values to the expected type before iterating/indexing,
  validate the parsed shape immediately (fail fast with a clear error), and explicitly
  handle sentinel/unknown states instead of “silently succeeding” with wrong assumptions.'
repository: awslabs/mcp
label: Null Handling
language: Python
comments_count: 4
repository_stars: 9545
---

Always treat nullable/optional fields and parsed payloads as untrusted at boundaries: normalize `None`/missing values to the expected type before iterating/indexing, validate the parsed shape immediately (fail fast with a clear error), and explicitly handle sentinel/unknown states instead of “silently succeeding” with wrong assumptions.

Apply this as a local rule:
- Prefer `for x in (value or [])` (or equivalent) when a field is “list-ish” but may be `null`.
- Before calling string/number methods, check element types (e.g., only `.lower()` strings).
- After `json.loads`/spec parsing, verify the root/object shape (e.g., dict/mapping) before using keys.
- If a classification can be `unknown`/unresolvable, return an explicit structured error or `platform: 'unknown'`+hint; don’t proceed with the “web/mobile” logic.

Example (list field that may be absent, `null`, or contain bad entries):
```python
from collections import defaultdict
from typing import Any

def index_tags(dataset: dict[str, Any]) -> dict[str, list[int]]:
    tag_index: dict[str, list[int]] = defaultdict(list)
    tags = dataset.get('Tags') or []  # handles missing or null
    if not isinstance(tags, list):
        raise ValueError("Tags must be a list when present")

    for tag in tags:
        if not isinstance(tag, str):
            continue  # or raise, depending on policy
        tag_index[tag.lower()].append(0)

    return tag_index
```

Example (parsed payload root validation):
```python
def require_mapping(obj: object) -> dict:
    if not isinstance(obj, dict):
        raise ValueError(f"Expected a mapping at the root, got {type(obj).__name__}")
    return obj

spec = require_mapping(parsed_spec)  # only then do spec['openapi'] checks
```

Outcome: fewer crashes on `null`, fewer opaque downstream TypeErrors, and safer behavior when inputs are missing or unresolved.