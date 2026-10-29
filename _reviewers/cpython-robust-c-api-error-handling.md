---
title: Robust C API error handling
description: 'When writing C extension/interpreter code, treat every fallible C API
  call as a potential failure point and handle it consistently:


  - **Check return values immediately.** After calling functions like `PyNumber_Subtract`,
  `PyLong_AsLong`, `PyObject_GetAttrString`, etc., check for failure before using
  the result. Don''t assume a prior check covers a later...'
repository: python/cpython
label: Error Handling
language: C
comments_count: 12
repository_stars: 77696
---

When writing C extension/interpreter code, treat every fallible C API call as a potential failure point and handle it consistently:

- **Check return values immediately.** After calling functions like `PyNumber_Subtract`, `PyLong_AsLong`, `PyObject_GetAttrString`, etc., check for failure before using the result. Don't assume a prior check covers a later re-invocation of the same API.
- **Use the documented failure idiom.** For APIs like `PyLong_AsLong`/`PyLong_AsInt` where a valid value can coincide with the sentinel, check `value == -1 && PyErr_Occurred()` rather than a bare `PyErr_Occurred()`, so you don't misinterpret a stale error flag or a legitimate `-1` result.
- **Prefer unambiguous APIs.** Choose APIs with clear success/failure signaling (e.g. `PyIter_NextItem` over `PyIter_Next`) to avoid ambiguity between "no result" and "error".
- **Propagate escaping calls outside of control flow.** When a call can set an exception (an "escaping call"), capture its result in a variable first, then branch on it, rather than embedding the call inside an `if`/loop condition. This keeps error propagation explicit and consistent with tier-2/JIT expectations.
- **Validate externally-supplied or untrusted values at runtime, not with `assert`.** Values coming from arbitrary Python objects (e.g. a `fold` or `year` attribute) must be range-checked with real error handling (`PyErr_Format(PyExc_ValueError, ...)`), since `assert` can be compiled out and casts to narrower types are undefined behavior if the value is out of range.
- **Match exception types and messages to documented behavior.** If two code paths handle the same underlying failure, make them consistent (e.g. both return an empty result or both raise), and raise exception types that calling code expects (e.g. don't let an unexpected `ValueError` escape where callers only catch `RuntimeError`).
- **Clean up all acquired resources on every exit path**, including early returns inside loops/branches, without double-freeing references that were already stolen or released elsewhere (e.g. after `PyList_SetSlice`/`extend`-like calls that steal references on failure, don't additionally `Py_DECREF`; add an assert/comment to document why).

Example of correct failure-check idiom and resource cleanup:

```c
long fold_int = PyLong_AsLong(fold_obj);
Py_DECREF(fold_obj);
if (fold_int == -1 && PyErr_Occurred()) {
    return NULL;
}
if (fold_int < 0 || fold_int > 1) {
    PyErr_Format(PyExc_ValueError, "fold must be 0 or 1, got %ld", fold_int);
    return NULL;
}
fold = (unsigned char)fold_int;
```

Applying this consistently prevents silent data corruption from unchecked UB casts, memory leaks/double-frees on error paths, and confusing failures where errors are swallowed, misclassified, or propagate inconsistently.