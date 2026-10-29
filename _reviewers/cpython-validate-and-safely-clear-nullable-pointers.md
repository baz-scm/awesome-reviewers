---
title: Validate and safely clear nullable pointers
description: In C extension code, every pointer that can legitimately be NULL (e.g.,
  the result of PyObject_GetAttr, PyNumber_Add, or other APIs that may fail) must
  be checked for NULL immediately before it is dereferenced or passed to another API
  call. Do not assume an "unlikely to fail" call always succeeds—an unchecked NULL
  result can lead to a null dereference or...
repository: python/cpython
label: Null Handling
language: C
comments_count: 4
repository_stars: 77696
---

In C extension code, every pointer that can legitimately be NULL (e.g., the result of PyObject_GetAttr, PyNumber_Add, or other APIs that may fail) must be checked for NULL immediately before it is dereferenced or passed to another API call. Do not assume an "unlikely to fail" call always succeeds—an unchecked NULL result can lead to a null dereference or crash, as seen when PyObject_GetAttr(spec, "origin") returned NULL and the code proceeded to use it, or when Py_SETREF(b, PyNumber_Add(...)) left b NULL before a subsequent PyNumber_Subtract call.

When cleaning up such pointers, use the NULL-safe macros (Py_XDECREF, Py_CLEAR) rather than Py_DECREF, since Py_DECREF on NULL is undefined/forbidden. Prefer a single cleanup path (e.g., a shared `error:`/`done:` label) that calls Py_XDECREF on all possibly-unset objects, rather than duplicating decref logic in every branch:

```c
PyObject *res = NULL;
PyObject *root = _isqrt_rem(n, &rem);

if (root && rem) {
    res = PyTuple_Pack(2, root, rem);
}
Py_XDECREF(root);
Py_XDECREF(rem);
return res;
```

Applying this consistently prevents both null-dereference crashes and bugs from duplicated or incorrect cleanup code.