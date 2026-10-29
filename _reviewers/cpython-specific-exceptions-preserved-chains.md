---
title: Specific exceptions, preserved chains
description: When catching and converting exceptions, catch the narrowest exception
  type that applies rather than a broad `Exception` or bare `except:` unless you are
  immediately re-raising (bare `except:` is acceptable only when the original exception
  is re-raised unchanged). Overly broad catches hide programming errors and make debugging
  harder.
repository: python/cpython
label: Error Handling
language: Python
comments_count: 8
repository_stars: 77696
---

When catching and converting exceptions, catch the narrowest exception type that applies rather than a broad `Exception` or bare `except:` unless you are immediately re-raising (bare `except:` is acceptable only when the original exception is re-raised unchanged). Overly broad catches hide programming errors and make debugging harder.

When converting a low-level exception into a higher-level one, always preserve the original cause with `raise NewError(...) from original_exc` so the traceback and root cause remain visible to users and tests can assert on it. Only use `raise ... from None` to explicitly suppress chaining when not inside an `except` block or when the cause is truly irrelevant.

Never silently swallow exceptions (e.g. `except Exception: pass`) in situations where a failure should be visible to the caller or user—at minimum surface the error (print/log the traceback) before continuing, especially for user-provided hooks/callbacks, so failures aren't invisible. If a caller explicitly requests a specific behavior (e.g. `prebuilt=True`), a failure to satisfy that request should raise rather than silently falling back to different behavior.

Also ensure error paths perform the same cleanup (closing connections/files, releasing resources) that the success path would, so raising an exception doesn't leave resources in an inconsistent state.

Example:
```python
try:
    name = name.decode()
except UnicodeDecodeError as exc:
    raise ZipImportError(
        f"can't decode file name in Zip file: {archive!r}",
        path=archive) from exc
```
rather than:
```python
try:
    name = name.decode()
except UnicodeDecodeError:
    raise ZipImportError(
        f"can't decode file name in Zip file: {archive!r}",
        path=archive)
```
which discards the original `UnicodeDecodeError` and makes it harder to diagnose the real cause.</description>
</invoke>
