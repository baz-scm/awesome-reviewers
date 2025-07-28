---
title: Choose appropriate string types
description: Select the most efficient string type based on ownership and lifetime
  requirements to optimize memory usage and prevent safety issues. Use `StringRef`
  for parameters and when you don't need to own the string data, `std::string` when
  you need ownership and persistence, and avoid storing `Twine` objects as member
  variables.
repository: llvm/llvm-project
label: Performance Optimization
language: Other
comments_count: 2
repository_stars: 33702
---

Select the most efficient string type based on ownership and lifetime requirements to optimize memory usage and prevent safety issues. Use `StringRef` for parameters and when you don't need to own the string data, `std::string` when you need ownership and persistence, and avoid storing `Twine` objects as member variables.

Key guidelines:
- Use `StringRef` for function parameters when you only need to read the string
- Use `std::string` for member variables when you need to own and persist the data
- Never store `Twine` as a member variable - it doesn't own its underlying data and can cause memory violations
- Consider whether you're making unnecessary copies of constant strings

Example from the discussions:
```cpp
// Bad: Unnecessary string copy for constant data
class InvalidRSMetadataFormat {
  std::string ElementName;  // If always called with constants
};

// Good: Use StringRef when appropriate
class InvalidRSMetadataFormat {
  StringRef ElementName;  // For constant strings
};

// Bad: Dangerous storage of Twine
class GenericRSMetadataError {
  Twine Message;  // Can cause memory violations
};

// Good: Own the string data when needed
class GenericRSMetadataError {
  std::string Message;  // Safe ownership
};
```

This optimization reduces memory allocations, prevents unnecessary copying, and avoids potential memory safety issues while maintaining code correctness.