---
title: Deterministic exception handling
description: When handling errors, ensure (1) you don’t accidentally change which
  exception path fires, (2) recovery/cleanup is deterministic, and (3) any wrapping/aggregation
  preserves context and remains actionable.
repository: celery/celery
label: Error Handling
language: Python
comments_count: 10
repository_stars: 28464
---

When handling errors, ensure (1) you don’t accidentally change which exception path fires, (2) recovery/cleanup is deterministic, and (3) any wrapping/aggregation preserves context and remains actionable.

Practical rules:
- Preserve the correct control-flow: re-raise “retryable/critical” exceptions rather than catching and continuing.
- Keep blast radius small: if changing exception behavior inside a widely-used component is risky, re-raise or handle at the narrower call site.
- Make cleanup guaranteed: don’t let cleanup steps be skipped because an earlier step failed—split cleanup into separate try/except blocks.
- Preserve recovery state: reconnect/retry logic must honor original options (e.g., ack/no-ack), and re-register required resources (e.g., queues) so recovery is complete.
- Preserve error context and actionability:
  - Use accurate messages aligned with the actual subsystem.
  - Chain exceptions when wrapping (raise ... from exc) and only convert exception types when it improves user guidance.
  - When retry/fallback logic exists, use the higher-level paths that include retry/error handling (avoid internal helpers that bypass it).

Example (retryable vs aggregated failures + chaining):

```python
exceptions = []
for item in items:
    try:
        do_bind(item)
    except Exception as e:
        if isinstance(e, RETRIED_EXCEPTIONS):
            raise  # preserve intended retry/outer mechanism
        exceptions.append(e)

if exceptions:
    raise RuntimeError(
        "Binding failures occurred\n" + "\n".join(map(str, exceptions))
    )

# During failure-path cleanup:
try:
    hub.reset()
except Exception:
    pass
try:
    hub.timer.clear()  # must still run
except Exception:
    pass
```

Apply this standard whenever you touch error recovery, retry/fallback behavior, exception aggregation/wrapping, or shutdown/reconnect paths.