---
title: Preserve original exceptions
description: When a run or operation fails, the original exception is the most valuable
  piece of information available — never let secondary code (cleanup, accounting,
  logging, or re-wrapping) silently replace or obscure it.
repository: kyegomez/swarms#pi240310
label: Error Handling
language: Python
comments_count: 7
repository_stars: 7337
---

When a run or operation fails, the original exception is the most valuable piece of information available — never let secondary code (cleanup, accounting, logging, or re-wrapping) silently replace or obscure it.

- Non-essential bookkeeping that runs in a `finally` block (usage tracking, metrics, hooks) must never be allowed to raise past that block, since doing so overwrites the real exception/traceback with an unrelated one. Guard it explicitly:
```python
finally:
    if swarm is not None:
        try:
            self._add_usage(swarm)
        except Exception:  # usage accounting must never mask the run result
            pass
```
The same applies to any public hook parameter supplied by a caller (e.g. `usage_hook`): wrap the call, don't trust it to be exception-safe.

- When you must re-raise a lower-level error as a higher-level, more descriptive one (e.g. "X is not serializable"), always chain it with `raise NewError(...) from original_error` rather than discarding it. This keeps the full cause chain visible in the traceback for debugging deeply nested failures, instead of pointing only at the outermost frame.

- Avoid broad `try/except` blocks that convert real bugs into silent placeholders or swallow import/runtime errors. If a class or function fails to export or execute correctly, that failure should surface immediately (as an exception or a clear log) rather than being hidden — masking an error just moves the cost of discovering the bug to a later, harder-to-diagnose point. For example, don't wrap imports in try/except just to avoid an `ImportError`; fix the underlying issue instead.
- When a path naturally produces partial results before failing, prefer surfacing an explicit error over silently returning a truncated or misleading "success" value, and document the chosen behavior clearly rather than relying on an assumption that may not always hold.