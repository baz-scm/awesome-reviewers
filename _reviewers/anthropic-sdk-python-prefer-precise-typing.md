---
title: Prefer precise typing
description: Use precise types instead of `Any`, and avoid unnecessary `typing.cast`
  by relying on type-guard utilities and existing type narrowing. In tests, prefer
  the concrete pytest types/fixtures (e.g., `pytest.MonkeyPatch`) over broad `Any`.
repository: anthropics/anthropic-sdk-python
label: Code Style
language: Python
comments_count: 5
repository_stars: 3392
---

Use precise types instead of `Any`, and avoid unnecessary `typing.cast` by relying on type-guard utilities and existing type narrowing. In tests, prefer the concrete pytest types/fixtures (e.g., `pytest.MonkeyPatch`) over broad `Any`.

Apply this as a style rule:
- Don’t annotate parameters/locals as `Any` when a concrete type exists.
- If you’re doing `typing.cast` purely to satisfy typing after runtime checks, prefer type-guard helpers (e.g., `is_dict`, `is_list`) that narrow types.
- If static analysis (e.g., pyright) already succeeds without a cast, remove it.

Example:
```python
import pytest
import typing as t
from .typing_utils import is_dict, is_list

@pytest.mark.respx()
def test_something(monkeypatch: pytest.MonkeyPatch) -> None:
    ...

def _deep_merge_extra_fields(existing: object, new: object) -> object:
    if is_dict(existing) and is_dict(new):
        # type is narrowed by is_dict
        for k, v in new.items():
            ...
        return existing
    if is_list(existing) and is_list(new):
        # type is narrowed by is_list
        existing.extend(new)
        return existing
    return new
```
