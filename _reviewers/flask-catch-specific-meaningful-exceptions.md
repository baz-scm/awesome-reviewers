---
title: Catch specific, meaningful exceptions
description: When handling errors, catch the narrowest exception type that accurately
  represents the failure, and avoid broad `except:`/`except Exception` blocks that
  silently swallow errors or hide tracebacks needed for debugging. If a broad catch
  is truly required (e.g. Python 2 compatibility where exceptions may not derive from
  `BaseException`), make the intent...
repository: pallets/flask
label: Error Handling
language: Python
comments_count: 7
repository_stars: 75022
---

When handling errors, catch the narrowest exception type that accurately represents the failure, and avoid broad `except:`/`except Exception` blocks that silently swallow errors or hide tracebacks needed for debugging. If a broad catch is truly required (e.g. Python 2 compatibility where exceptions may not derive from `BaseException`), make the intent explicit in a comment and ensure the resulting behavior is still correct—don't let it mask unrelated bugs.

Avoid fragile heuristics such as matching on exception message text to decide how to react to an error (e.g. checking `str(exc_value).startswith(...)` to detect a wrong-arguments `TypeError`); these break easily and can misclassify errors raised by unrelated code. Prefer structural checks instead, such as inspecting the exception's type/traceback frames, e.g.:

```python
def _called_with_wrong_args(factory, exc_info):
    _, _, tb = exc_info
    while tb.tb_next:
        tb = tb.tb_next
    return tb.tb_frame.f_code.co_name == factory.__name__
```

When an error must be suppressed to keep a feature usable (e.g. not breaking `--help` if the app fails to import), catch only the specific exception that represents that known failure mode (like `NoAppException`) rather than `Exception`, and still surface a clear message to the user (via `print(..., file=sys.stderr)` or `warnings.warn`) instead of silently discarding the error or using ad-hoc `print`/`traceback.print_exc()` calls that bypass the normal error-reporting path. This keeps error handling predictable, preserves useful diagnostics, and prevents hidden bugs from being masked by overly permissive exception handling.