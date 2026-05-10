---
title: Semantic ordering guards
description: When code depends on ordering/selection (scheduling, routing, matching),
  implement it using *semantic* state and *explicit* guard windows—avoid brittle string
  checks and avoid guards that assume “typical” transition times.
repository: celery/celery
label: Algorithms
language: Python
comments_count: 4
repository_stars: 28464
---

When code depends on ordering/selection (scheduling, routing, matching), implement it using *semantic* state and *explicit* guard windows—avoid brittle string checks and avoid guards that assume “typical” transition times.

Apply this standard:
- **Use parsed semantics, not raw user input.** If you need to know whether an hour field is effectively “all hours,” check the parsed/normalized representation (e.g., `self.hour == set(range(24))`) rather than `self._orig_hour == '*'`.
- **Guard edge-case transitions with measurable windows.** For DST fall-back scheduling, require (a) offset direction change, (b) a short UTC proximity window, and (c) any additional constraints only if they are truly transition-safe.
- **Don’t overfit to “same calendar day” unless proven.** If DST can occur at midnight in some zones, `last_run_at.date() == now.date()` can block correctness; add tests and prefer guards that won’t fail at boundary transitions.
- **Define precedence for competing candidates by specificity.** For routing/matching, make precedence explicit (e.g., direct mapping > glob > regex) and/or derived specificity measures, and sort deterministically.

Example (DST guard—avoid brittle hour string checks):
```python
last_offset = last_run_at.utcoffset()
now_offset = now.utcoffset()

is_hourly = (self.hour == set(range(24)))  # semantic, parsed check

if (last_offset and now_offset and last_offset > now_offset and is_hourly):
    last_utc = last_run_at - last_offset
    now_utc = now - now_offset
    utc_delta = now_utc - last_utc

    # Keep the transition-aware UTC proximity window
    if timedelta(0) < utc_delta <= timedelta(hours=2):
        # Also verify via tests for midnight/rare transition boundaries
        ...
```

Teams should enforce this with targeted tests for DST-at-midnight scenarios and for “logically equivalent” crontab inputs (e.g., `'*'` vs `*/1`).