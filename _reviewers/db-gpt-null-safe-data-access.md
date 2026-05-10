---
title: Null-Safe Data Access
description: 'Write code so nullable/missing data can’t cause runtime errors.


  Apply these rules:

  1) Declare nullability in types

  - If a parameter or field defaults to `None`, type it as `Optional[...]`.'
repository: eosphoros-ai/DB-GPT
label: Null Handling
language: Python
comments_count: 6
repository_stars: 18703
---

Write code so nullable/missing data can’t cause runtime errors.

Apply these rules:
1) Declare nullability in types
- If a parameter or field defaults to `None`, type it as `Optional[...]`.

2) Use safe dict/JSON access
- If a key may be absent, prefer `dict.get("key")` instead of `dict["key"]`.

3) Guard empty sequences before indexing
- Before using `choices[0]`, `rows[0]`, etc., check the sequence is non-empty (and the expected object shape exists).

4) Use `is not None` instead of truthiness for config inclusion
- When deciding whether to include a config value, use `if value is not None:` so meaningful falsy values aren’t accidentally dropped.

Example:
```python
from typing import Optional

def parse_intent(payload: dict) -> Optional[str]:
    # key may be missing -> use get
    return payload.get("rewrited_question")

def handle_response(r):
    # choices may be missing/empty -> guard before indexing
    choices = r.get("choices") if isinstance(r, dict) else getattr(r, "choices", None)
    if not choices:
        return None
    first = choices[0]
    return getattr(first.delta, "content", None)

def build_config(cfg_obj):
    config_dict = {}
    for key in cfg_obj.model_dump().keys():
        value = getattr(cfg_obj, key)
        if value is not None:  # not: if value:
            config_dict[key] = value
    return config_dict
```

Outcome: fewer `KeyError`, `IndexError`, and silent config-misbehavior, while making null/empty cases explicit and testable.