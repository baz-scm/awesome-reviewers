---
title: Choose appropriate exceptions
description: 'Select the proper exception type based on the error scenario to provide
  clearer error handling and better debugging experience:


  1. Use ValueError (TORCH_CHECK_VALUE) when input parameters have invalid values'
repository: pytorch/pytorch
label: Error Handling
language: C++
comments_count: 4
repository_stars: 91345
---

Select the proper exception type based on the error scenario to provide clearer error handling and better debugging experience:

1. Use ValueError (TORCH_CHECK_VALUE) when input parameters have invalid values
2. Use RuntimeError (TORCH_CHECK) when user inputs are invalid in ways other than just their values (such as incompatible tensor properties)
3. Use AssertionError (TORCH_CHECK_ASSERT) for internal invariant violations
4. When working with C/Python API boundaries, explicitly check for null pointers and throw appropriate exceptions

Example:
```cpp
// For invalid parameter values
TORCH_CHECK_VALUE(
    at::isFloatingType(count.scalar_type()),
    "binomial only supports floating-point dtypes for count, got: ",
    count.scalar_type());

// For other input validation
TORCH_CHECK(
    indices.is_pinned() == values.is_pinned(),
    "memory pinning of indices must match memory pinning of values");

// For internal invariants
TORCH_INTERNAL_ASSERT(r.idx == 0, "Unexpected parser result");

// For C API null checks
PyObject* tuple = PyTuple_New(2);
if (!tuple) {
  throw python_error();
}
```

Using appropriate exception types helps users better understand and handle errors, improves API clarity, and facilitates more effective debugging. Proper error messages that describe the problem and expected behavior enable users to quickly identify and fix issues.