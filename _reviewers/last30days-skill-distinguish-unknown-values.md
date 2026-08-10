---
title: Distinguish Unknown Values
description: When data fields can be missing, placeholder, or truly empty, never collapse
  them into the same falsy value. Explicitly represent and branch on “unknown vs empty”
  (or verified vs unverified), and avoid `if x:` checks that treat `0`/`""`/`None`
  equivalently.
repository: mvanhorn/last30days-skill
label: Null Handling
language: Python
comments_count: 6
repository_stars: 57799
---

When data fields can be missing, placeholder, or truly empty, never collapse them into the same falsy value. Explicitly represent and branch on “unknown vs empty” (or verified vs unverified), and avoid `if x:` checks that treat `0`/`""`/`None` equivalently.

Apply these rules:
- Use `is None`/`is not None` for optional numeric overrides and nullable fields so an explicit `0` is honored.
- Introduce a verification flag (e.g., `counts_verified`) or a distinct sentinel (`None`) instead of overloading `0` as both “unknown” and “empty”.
- In tiering/ranking logic, base decisions on the verification status (or a verified count), not on proxies like “score implies count”.
- For string extraction, handle `null`/missing fields by defaulting to `""` only at the leaf (e.g., `str(x.get(...) or "")`).
- For identity/refetch flows, fail closed when required identity is absent (don’t proceed on partial matches).

Example (verified vs placeholder count):
```py
def payoff_tier(post):
    eng = post.get("engagement") or {}
    if eng.get("counts_verified"):
        # real count: treat 0 as empty, >0 as non-empty
        return 2 if (eng.get("num_comments") or 0) > 0 else 0
    # unknown count (placeholder): don’t penalize as empty
    return 1

# Optional numeric override: honor explicit 0
cap = config.get("_max_source_fetches")
if cap is not None:
    cap = int(cap)
```