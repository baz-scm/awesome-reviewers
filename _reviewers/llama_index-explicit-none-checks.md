---
title: Explicit none checks
description: Several bugs stemmed from conflating `None` with other falsy values (`0`,
  `""`, `False`) or from inconsistent handling of optional parameters. When a parameter's
  default or current value is semantically different from "missing" (e.g. `max_iterations=0`,
  `threshold=0.0`, `similarity_cutoff=None`), do not rely on truthy/`or` checks —
  use explicit `is None` /...
repository: run-llama/llama_index
label: Null Handling
language: Python
comments_count: 8
repository_stars: 52785
---

Several bugs stemmed from conflating `None` with other falsy values (`0`, `""`, `False`) or from inconsistent handling of optional parameters. When a parameter's default or current value is semantically different from "missing" (e.g. `max_iterations=0`, `threshold=0.0`, `similarity_cutoff=None`), do not rely on truthy/`or` checks — use explicit `is None` / `is not None` comparisons:

```python
# Bad: 0 is falsy, so this silently falls back to the default
max_iterations = ev.get("max_iterations", default=None) or DEFAULT_MAX_ITERATIONS

# Good: only fall back when the value is actually missing
max_iterations = ev.get("max_iterations", default=None)
if max_iterations is None:
    max_iterations = DEFAULT_MAX_ITERATIONS
```

The same applies to optional thresholds/cutoffs used in comparisons (`similarity_cutoff`, `threshold`): guard every comparison with an explicit `is None` check before using it, and keep the default value and comparison semantics (e.g. `>` vs `>=`) consistent across all functions that use the same parameter, documenting the chosen default.

When reading optional values from a dict (e.g. `kwargs`), never index directly (`kwargs["store"]`) since a missing key raises `KeyError`; use `kwargs.get("store")` or `payload.setdefault("stream", stream)` so the call degrades gracefully when the key is absent instead of only when its value is `None`.

Finally, keep type hints honest about nullability: if a parameter or return value can be `None`, annotate it as `Optional[T]` (or `T | None`) rather than defaulting to `None` while declaring the type as non-optional, and type placeholder containers that may hold `None` accordingly (e.g. `List[Optional[List[float]]]`). This keeps static type checkers useful and makes it obvious to callers where `None` is a valid, expected value versus an error condition.