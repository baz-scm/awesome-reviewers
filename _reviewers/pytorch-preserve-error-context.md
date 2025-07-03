---
title: Preserve error context
description: When handling errors, always preserve rich contextual information to
  make debugging easier and error messages more meaningful. This includes maintaining
  call site information, error codes, and detailed messages that explain what went
  wrong.
repository: pytorch/pytorch
label: Error Handling
language: Other
comments_count: 3
repository_stars: 91169
---

When handling errors, always preserve rich contextual information to make debugging easier and error messages more meaningful. This includes maintaining call site information, error codes, and detailed messages that explain what went wrong.

For C/C++ code:
1. Use error handling mechanisms that preserve context (like `TORCH_CHECK_WITH` instead of simple throws)
2. When working with C APIs, always check return values and convert failures to exceptions with appropriate context
3. For language boundaries (C++/Python), ensure proper exception translation to maintain error information

Example:
```cpp
// Check return values from C API functions
PyObject* tuple = PyTuple_New(2);
if (!tuple) {
  throw python_error(); // Convert C API failure to C++ exception with context
}

// Use appropriate error checking with detailed messages
TORCH_CHECK(
  THPDevice_Check(data),
  "torchDeviceToDLDevice: expected torch.device argument.");

// When crossing language boundaries, use proper translation mechanisms
// like END_HANDLE_TH_ERRORS to ensure C++ exceptions become appropriate Python exceptions
```

This approach ensures that when errors occur, developers have the information they need to understand and fix the issue quickly.
