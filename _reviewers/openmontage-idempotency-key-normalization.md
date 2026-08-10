---
title: Idempotency key normalization
description: 'When implementing caching/idempotency for tools that generate external
  media, make cache keys stable and semantically accurate.


  **Rules**

  1. **Normalize before hashing:** Resolve optional fields through `input_schema`
  defaults; treat an explicit `None` as “unset”, so omitted and defaulted inputs produce
  the same key.'
repository: calesthio/OpenMontage
label: Caching
language: Python
comments_count: 2
repository_stars: 46544
---

When implementing caching/idempotency for tools that generate external media, make cache keys stable and semantically accurate.

**Rules**
1. **Normalize before hashing:** Resolve optional fields through `input_schema` defaults; treat an explicit `None` as “unset”, so omitted and defaulted inputs produce the same key.
2. **Hash only what changes output:** `idempotency_key_fields` should include only fields that are actually consumed by the request/output builders. Do **not** include fields the provider ignores, or you’ll get false cache misses.
3. **Test key behavior:** Add tests for both:
   - **Stability:** inputs that differ only by omitted/defaulted values produce identical keys.
   - **Sensitivity:** inputs that truly change the generated result produce different keys.

**Example pattern**
```python
class MyTool(BaseTool):
    input_schema = {
        "type": "object",
        "required": ["prompt"],
        "properties": {
            "prompt": {"type": "string"},
            "prompt_influence": {"type": "number", "default": 0.3},
            "loop": {"type": "boolean", "default": False},
        },
    }

    # Include only fields that affect the request/output
    idempotency_key_fields = ["prompt", "prompt_influence", "loop"]
```

This ensures cache/idempotency behaves predictably: no accidental misses from default handling, and no accidental hits from hashing irrelevant fields.