---
title: Deterministic Parse-Merge Rules
description: 'When writing parsing or data-merge algorithms, ensure the logic is context-aware
  and unambiguous:


  - Scope semantics to the correct regions. If a formatter/markup has “non-semantic”
  contexts (e.g., fenced code blocks), your parser must ignore content inside them
  and only interpret the intended regions.'
repository: bmad-code-org/bmad-method
label: Algorithms
language: Python
comments_count: 2
repository_stars: 51859
---

When writing parsing or data-merge algorithms, ensure the logic is context-aware and unambiguous:

- Scope semantics to the correct regions. If a formatter/markup has “non-semantic” contexts (e.g., fenced code blocks), your parser must ignore content inside them and only interpret the intended regions.
- Make special-case behavior conditional on strict preconditions. Apply keyed/structured merging or interpretation only when the input satisfies the full contract (e.g., all array items use the same identifier key); otherwise use a conservative fallback (e.g., append) rather than guessing.
- Document the contract and fallback behavior so contributors don’t accidentally reintroduce ambiguity.
- Add regression tests specifically for boundary cases (e.g., headings/rows inside fences; mixed-key arrays).

Example (keyed array merge precondition + safe fallback):
```python
def keyed_array_merge(base_items, override_items, keyed_fields=("code", "id")):
    def detect_key(items):
        if not items or not all(isinstance(x, dict) for x in items):
            return None
        for k in keyed_fields:
            if all(item.get(k) is not None for item in items):
                return k
        return None

    key = detect_key(base_items) or detect_key(override_items)
    if key is None:
        # ambiguous schema: append by design
        return list(base_items) + list(override_items)

    # keyed merge (deterministic)
    index = {item[key]: item for item in base_items}
    result = list(base_items)
    for o in override_items:
        oid = o[key]
        if oid in index:
            # replace existing
            replace_at = result.index(index[oid])
            result[replace_at] = o
        else:
            result.append(o)
            index[oid] = o
    return result
```
