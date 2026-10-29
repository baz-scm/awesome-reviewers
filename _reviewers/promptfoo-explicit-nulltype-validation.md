---
title: Explicit null/type validation
description: 'When consuming loosely-typed or external data (parsed JSON, optional
  fields, etc.), never rely on Python truthiness to decide whether a value is "present"
  or "valid" — it conflates `None`/missing with legitimate falsy values (e.g. `0`,
  `""`, `[]`) and can let malformed data through un-validated. Instead:'
repository: promptfoo/promptfoo
label: Null Handling
language: Python
comments_count: 5
repository_stars: 26565
---

When consuming loosely-typed or external data (parsed JSON, optional fields, etc.), never rely on Python truthiness to decide whether a value is "present" or "valid" — it conflates `None`/missing with legitimate falsy values (e.g. `0`, `""`, `[]`) and can let malformed data through un-validated. Instead:

1. Use `isinstance(x, ExpectedType)` checks before using a value's type-specific behavior (e.g. calling `.strip()`, set-membership checks, or `is True`/`False` comparisons). A non-string `text`, a non-string `kind`, or a non-boolean `ok` should never be treated as if it were the expected type.
2. Distinguish "absent" from "falsy-but-valid" with `is not None` rather than `if value:`. For example, a numeric `topic` of `0` must still be treated as a real topic, not dropped.
3. Validate collection/item shapes up front (e.g. ensure every item in a list of steps is a `dict` with required string keys) and short-circuit to a safe, documented fallback path rather than letting later code raise on malformed members (e.g. `None`, lists where dicts are expected).
4. When data fails validation, default to a fail-closed outcome (treat as missing/invalid/low-quality) rather than fail-open (treat as valid/successful), especially in grading, security, or validation logic.

Example:
```python
def _has_content(s: dict[str, Any]) -> bool:
    text = s.get("text", "")
    return isinstance(text, str) and bool(text.strip())

def _is_annotated_ok(step: dict[str, Any]) -> bool:
    ok = step.get("ok")
    return isinstance(ok, bool) and ok  # non-bool values fail closed

topics = [s.get("topic") for s in steps if s.get("topic") is not None]  # keep 0
```

Apply this pattern whenever parsing external input, optional fields, or dynamic/untyped data structures to prevent null-reference crashes and subtle correctness bugs from type coercion or truthiness shortcuts.