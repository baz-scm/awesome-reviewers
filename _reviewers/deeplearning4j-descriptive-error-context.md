---
title: Descriptive error context
description: Error messages should be specific, descriptive, and include context to
  help with debugging. Avoid generic messages like "Failed execution" or numeric error
  codes without explanation.
repository: deeplearning4j/deeplearning4j
label: Error Handling
language: C++
comments_count: 5
repository_stars: 14036
---

Error messages should be specific, descriptive, and include context to help with debugging. Avoid generic messages like "Failed execution" or numeric error codes without explanation.

Key principles:
1. Always include the class/method name in error messages: `ShapeList::push_back: ShapeList limit exceeded`
2. Provide relevant variable values and expected conditions: `Expected type FLOAT32, but got INT32`
3. Use explicit errors for edge cases rather than silent handling
4. Format complex data types in human-readable form

Example with improved error messaging:
```cpp
// Poor error message
if (size() <= idx || idx < 0) 
  throw std::runtime_error("Can't find requested variable by index");

// Better error message
if (size() <= idx || idx < 0) 
  throw std::runtime_error(
    std::string("ShapeList::at: Index out of bounds, requested: ") + 
    std::to_string(idx) + " but size is: " + std::to_string(size())
  );
```

For assertions in lower-level code that might be called from higher-level languages like Java, include descriptive messages that don't require reading C++ code to understand the error condition.