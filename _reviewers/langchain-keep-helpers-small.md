---
title: Keep Helpers Small
description: Favor readability and maintainability by keeping functions/methods short,
  extracting complex logic into well-named helpers, and avoiding duplicated or closure-based
  implementations in constructors.
repository: langchain-ai/langchain
label: Code Style
language: Python
comments_count: 8
repository_stars: 136312
---

Favor readability and maintainability by keeping functions/methods short, extracting complex logic into well-named helpers, and avoiding duplicated or closure-based implementations in constructors.

Apply these rules:
- If a function becomes hard to follow (deep nesting, multiple loops/branches, “lost focus”), extract parts into private helper functions (or a small builder object).
- Remove duplication (e.g., sync vs async wrappers) by sharing the core logic in one helper.
- Avoid putting substantial tool implementations/behavior inside `__init__` as closures; create private methods (or module-level functions) and wire them in from `__init__`.
- Keep imports at module top-level; avoid mid-file imports unless there’s a deliberate reason (e.g., `TYPE_CHECKING` blocks).
- When writing multiline literals, watch for trailing commas that can accidentally turn strings into tuples.

Example (extracting complex logic into helpers):
```python
def _merge_reasoning_details(details: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if len(details) <= 1:
        return details

    merged: list[dict[str, Any]] = []
    i = 0
    while i < len(details):
        entry = details[i]
        if not _is_mergeable_fragment(entry):
            merged.append(entry)
            i += 1
            continue

        entry_type, entry_index, text_key = _fragment_key(entry)
        base = _fragment_base(entry, text_key)
        texts = [_fragment_text(entry, text_key)]

        i += 1
        while i < len(details) and _matches_fragment(details[i], entry_type, entry_index):
            texts.append(details[i].get(text_key, "") or "")
            base = _merge_fragment_metadata(base, details[i], text_key)
            i += 1

        merged.append({**base, text_key: "".join(texts)})

    return merged
```
