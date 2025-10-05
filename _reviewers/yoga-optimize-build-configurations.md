---
title: Optimize build configurations
description: When configuring CMake builds, carefully select compiler and linker flags
  that optimize for performance while maintaining cross-platform compatibility. Performance-oriented
  flags can significantly impact runtime speed, binary size, and resource utilization,
  but must be applied conditionally based on the target platform and compiler.
repository: facebook/yoga
label: Performance Optimization
language: Txt
comments_count: 3
repository_stars: 18255
---

When configuring CMake builds, carefully select compiler and linker flags that optimize for performance while maintaining cross-platform compatibility. Performance-oriented flags can significantly impact runtime speed, binary size, and resource utilization, but must be applied conditionally based on the target platform and compiler.

Key practices:
- Research the performance implications of compilation flags before applying them (e.g., `DYNAMIC_EXECUTION=0` may slow down WebAssembly bindings)
- Use conditional compilation to apply platform-specific optimizations (e.g., `--gc-sections` for GCC/Clang vs `--dead_strip` for AppleClang)
- Enable standard performance flags like `CMAKE_POSITION_INDEPENDENT_CODE ON` for better code generation
- Consider alternative optimization strategies when default flags cause performance regressions

Example of conditional linker optimization:
```cmake
target_link_options(yoga PRIVATE
    # Discard unused sections
    $<$<CONFIG:RELEASE>:$<$<CXX_COMPILER_ID:Clang,GNU>:-Wl,--gc-sections>>
    $<$<CONFIG:RELEASE>:$<$<CXX_COMPILER_ID:AppleClang>:-Wl,-dead_strip>>)
```

This approach ensures optimal performance across different build environments while avoiding platform-specific build failures.