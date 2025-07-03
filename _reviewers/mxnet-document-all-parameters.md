---
title: Document all parameters
description: Always provide complete and accurate documentation for all function parameters,
  especially when adding new ones. Each parameter should have a clear description
  that explains its purpose, expected values, and behavior.
repository: apache/mxnet
label: Documentation
language: Other
comments_count: 5
repository_stars: 20801
---

Always provide complete and accurate documentation for all function parameters, especially when adding new ones. Each parameter should have a clear description that explains its purpose, expected values, and behavior.

When adding a new parameter to an existing function:
1. Add documentation that clearly states what the parameter does
2. Explain any default behavior or special conditions
3. Use consistent formatting across similar functions

For example, when adding a parameter like `failsafe`:

```cpp
/**
 * \brief Allocation.
 * \param handle Handle struct.
 * \param failsafe Return a handle with a null dptr if out of memory, rather than exit.
 */
virtual void Alloc(Storage::Handle* handle, bool failsafe = false);
```

This helps other developers understand how to use the function correctly and makes the codebase more maintainable. Incomplete parameter documentation can lead to misuse of functions and introduces bugs that are difficult to diagnose.
