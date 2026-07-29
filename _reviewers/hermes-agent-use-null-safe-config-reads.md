---
title: Use Null-Safe Config Reads
description: 'Treat every potentially-null/nullable config subsection and external
  payload field as untrusted: normalize it before accessing deeper keys or calling
  methods.'
repository: nousresearch/hermes-agent
label: Null Handling
language: Python
comments_count: 9
repository_stars: 221948
---

Treat every potentially-null/nullable config subsection and external payload field as untrusted: normalize it before accessing deeper keys or calling methods.

**Rules**
- When reading nested config, guard for both missing keys and `null` subsections (common in YAML):
  - Prefer `section = cfg.get("x") or {}` before `section.get(...)`.
- When reading config values that might be the wrong type (e.g., mapping expected but boolean provided), validate the shape:
  - Use `isinstance(value, dict)` (or equivalent) before nested `.get()`.
- When using external event fields, validate types before string operations (e.g., `startswith`):
  - Check `isinstance(field, str)`.
- Ensure annotation types referenced in runtime-evaluated modules are imported (avoid `NameError` from `Optional`/`Any`).

**Example**
```python
def pick_language(stt_config: dict) -> str | None:
    stt_config = stt_config or {}
    groq_cfg = stt_config.get("groq") or {}          # handles groq: null
    local_cfg = stt_config.get("local") or {}
    return groq_cfg.get("language") or local_cfg.get("language")

def handle_matrix_location(payload: dict) -> None:
    geo_uri = payload.get("geo_uri")
    if not isinstance(geo_uri, str):
        return  # or safely log/drop
    if geo_uri.startswith("geo:"):
        ...
```

This prevents crashes like `AttributeError: 'NoneType' object has no attribute 'get'` and `AttributeError`/`TypeError` from calling string methods on non-strings.