---
title: Specific, informative exception handling
description: 'Avoid broad or bare `except` clauses that silently swallow errors or
  catch unrelated failures like `SystemExit` or `KeyboardInterrupt`. Only catch the
  specific exception types you expect and know how to handle; let everything else
  propagate so bugs are not hidden. For example, prefer:'
repository: pallets/flask#x
label: Error Handling
language: Python
comments_count: 8
repository_stars: 75163
---

Avoid broad or bare `except` clauses that silently swallow errors or catch unrelated failures like `SystemExit` or `KeyboardInterrupt`. Only catch the specific exception types you expect and know how to handle; let everything else propagate so bugs are not hidden. For example, prefer:

```python
try:
    data = dict(*args, **kwargs)
except (TypeError, ValueError) as e:
    raise BadRequest(str(e))
```

over a bare `except:` or `except Exception:` that discards the error.

When raising errors, use the exception type that matches the failure (e.g. `ValueError` for invalid arguments, `RuntimeError` for invalid runtime state) instead of generic exceptions or `assert`, which can be stripped in optimized mode and gives unclear feedback. Error messages should include enough context (e.g. the invalid value, the parsed JSON failure reason) to let the developer quickly understand the cause, especially in debug mode—don't reduce a detailed exception into a generic one without useful detail.

Avoid fragile heuristics (such as string-matching exception messages) to classify errors; inspect the traceback or exception type directly when precise detection is required. If code depends on an optional dependency, fail fast with a clear, actionable message (e.g. `raise RuntimeError("Install asgiref in order to run async views.")`) instead of letting an unrelated `ImportError` surface deep in the call stack.