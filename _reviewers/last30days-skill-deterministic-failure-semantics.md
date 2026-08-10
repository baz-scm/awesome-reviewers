---
title: Deterministic Failure Semantics
description: 'Treat error handling as deterministic control flow: classify outcomes
  precisely, set gating flags/budgets before the expensive/remote work, and use those
  classifications to decide whether to fall back/retry.'
repository: mvanhorn/last30days-skill
label: Error Handling
language: Python
comments_count: 6
repository_stars: 57799
---

Treat error handling as deterministic control flow: classify outcomes precisely, set gating flags/budgets before the expensive/remote work, and use those classifications to decide whether to fall back/retry.

Practical rules:
- **Set authoritative mode flags early**: If a lookup is explicitly pinned/authoritative, ensure the rest of the pipeline knows it *before* running the lookup. Empty results should produce a specific “no-results” failure and **must suppress** generic fan-out/retry; exceptions should preserve their original failure type/detail.
- **Never downgrade a success because earlier fallbacks failed**: In multi-backend fallback, earlier backend errors are observability only (log to stderr) when a later backend succeeds; only mark degraded when the producing backend truly fails.
- **Preserve user-edited artifacts on regeneration**: Before overwriting generated files, check for a generator marker; if absent, move the existing file to a non-clobbering `.bak/.bakN` (first free name) and write the new output.
- **Start retry/timeout budgets at the right phase**: Begin timers after required prerequisites (e.g., session readiness) so warm-up doesn’t consume the retry budget.
- **Make external steps cleanup-safe**: Avoid shell constructs that can abort before cleanup under strict modes (`set -e`, differing shells). Prefer safe file selection patterns (e.g., `find ... | head -1`) and add regression guards against reintroducing unsafe patterns.

Example pattern (authoritative gating):
```python
person_done = True  # set before authoritative lookup
try:
    items = fetch_pinned_user(...)
    if not items:
        bundle.record_failure(
            "github", "no-results", f"Person mode found no activity for @{user}"
        )
    return items
except Exception as e:
    bundle.record_failure("github", "pinned-lookup-error", str(e))
    raise
# downstream must check person_done to suppress generic fan-out/retry
```