---
title: Cleanup before errors
description: Always ensure all resources are properly released before raising errors
  to prevent resource leaks. This practice is essential for maintaining system stability
  and avoiding memory leaks in both normal and error conditions.
repository: opencv/opencv
label: Error Handling
language: Other
comments_count: 3
repository_stars: 82865
---

Always ensure all resources are properly released before raising errors to prevent resource leaks. This practice is essential for maintaining system stability and avoiding memory leaks in both normal and error conditions.

When handling errors, follow this pattern:
1. Set an error flag when an error condition is detected
2. Perform all necessary cleanup operations
3. Only then raise the actual error

This approach is particularly important when working with external resources like Python references, locks, file handles, and memory allocations.

For example, instead of immediately raising an error:

```cpp
// BAD: Error raised before cleanup is performed
if (!PyObject_IsInstance(obj, type))
    CV_Error(cv::Error::StsBadArg, "Input stream should be derived from io.BufferedIOBase");
// The GIL is never released and 'type' reference is leaked
```

Set a flag, perform cleanup, then raise the error:

```cpp
// GOOD: Cleanup performed before raising error
bool has_error = false;
if (!PyObject_IsInstance(obj, type))
    has_error = true;

// Cleanup resources regardless of error
Py_DECREF(type);
PyGILState_Release(gstate);

// Raise error after cleanup
if (has_error)
    CV_Error(cv::Error::StsBadArg, "Input stream should be derived from io.BufferedIOBase");
```

This pattern applies to all error scenarios, whether using exceptions (like CV_Error), assertions (CV_Assert), or returning error codes. By ensuring resources are released before propagating errors, you create more robust code that can handle failure scenarios gracefully.
