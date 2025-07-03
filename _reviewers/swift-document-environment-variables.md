---
title: Document environment variables
description: When using configurable components, clearly document all relevant environment
  variables and their effects. Include examples showing how to set variables for common
  use cases, and specify any platform-specific differences. For environment variables
  that affect runtime behavior, clearly document when they need to be set and any
  order dependencies.
repository: tensorflow/swift
label: Configurations
language: Other
comments_count: 4
repository_stars: 6136
---

When using configurable components, clearly document all relevant environment variables and their effects. Include examples showing how to set variables for common use cases, and specify any platform-specific differences. For environment variables that affect runtime behavior, clearly document when they need to be set and any order dependencies.

For example, when documenting Python interoperability configuration:

```swift
// Environment variables for Python configuration:
// PYTHON_LIBRARY="~/anaconda3/lib/libpython3.7m.so" - Sets specific Python library (takes precedence)
// PYTHON_VERSION="3.7" - Searches system paths for this Python version
// PYTHON_LOADER_LOGGING=1 - Enables debug output for Python library loading

// Note: Version selection must occur before any Python code is executed
import Python
// PythonLibrary.useVersion(3, 7)  // Must be called immediately after import

print(Python.version)  // Now safe to use Python
```

Note platform-specific variations when they exist, as with the Python library path example: "The exact filename will differ across Python environments and platforms." Including such details helps users successfully configure their environment regardless of their system.
