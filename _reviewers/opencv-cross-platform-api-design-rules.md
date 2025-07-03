---
title: Cross-platform API design rules
description: 'Design public APIs to work seamlessly across different programming languages
  and platforms. Follow these key principles:


  1. Use platform-agnostic types in public interfaces:'
repository: opencv/opencv
label: API
language: Other
comments_count: 6
repository_stars: 82865
---

Design public APIs to work seamlessly across different programming languages and platforms. Follow these key principles:

1. Use platform-agnostic types in public interfaces:
   - Prefer `int` over `size_t` for array sizes and indices
   - Avoid unsigned types that don't translate well to other languages
   - Use explicit size types (int32_t, int64_t) when specific sizes are required

2. Add proper binding annotations for cross-language support:
```cpp
class CV_EXPORTS_W MyClass {
public:
    CV_WRAP void process(int size);  // Not size_t
    CV_WRAP_AS(processBytes) Mat process(InputArray data);  // Alias for clarity
};
```

3. Avoid passing language-specific objects through plugin/module boundaries:
   - Don't pass STL containers or C++ objects through plugin APIs
   - Use C-style interfaces or abstract base classes for plugin APIs
   - Consider providing factory functions for complex objects

4. Maintain binary compatibility:
   - Don't modify existing function signatures
   - Create new overloads or functions for extended functionality
   - Document API version changes clearly

Following these guidelines ensures your API works reliably across Python, Java, and C++ while maintaining long-term stability.
