---
title: Document algorithmic reasoning
description: 'When implementing algorithms that involve data transformations, platform-specific
  behavior, or non-obvious computational choices, always include comments explaining
  the underlying reasoning and assumptions. This is especially critical for:'
repository: bazelbuild/bazel
label: Algorithms
language: Other
comments_count: 2
repository_stars: 24489
---

When implementing algorithms that involve data transformations, platform-specific behavior, or non-obvious computational choices, always include comments explaining the underlying reasoning and assumptions. This is especially critical for:

- Data format conversions (endianness, serialization)
- Platform or compiler-specific algorithmic variations
- Complex bit manipulations or mathematical transformations
- Performance optimizations that sacrifice readability

The explanation should clarify why the algorithm is necessary, what assumptions it makes about the data or environment, and any relevant technical context that future maintainers might lack.

Example:
```cpp
// JVM class files use big-endian byte order, but x86/ARM systems are little-endian.
// This function converts between the two representations when reading binary data.
template<typename T>
inline static T swapByteOrder(const T& val) {
  int totalBytes = sizeof(val);
  T swapped = (T) 0;
  for (int i = 0; i < totalBytes; ++i) {
    swapped |= (val >> (8*(totalBytes-i-1)) & 0xFF) << (8*i);
  }
  return swapped;
}
```

Without such documentation, algorithmic choices appear arbitrary and create maintenance burdens for developers who lack the original context.