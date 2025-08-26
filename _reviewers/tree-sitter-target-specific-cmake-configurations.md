---
title: target-specific CMake configurations
description: Use target-specific CMake commands instead of global ones to ensure proper
  scoping and avoid polluting the global build environment. This improves maintainability
  and prevents unintended side effects when building multiple targets.
repository: tree-sitter/tree-sitter
label: Configurations
language: Txt
comments_count: 2
repository_stars: 21799
---

Use target-specific CMake commands instead of global ones to ensure proper scoping and avoid polluting the global build environment. This improves maintainability and prevents unintended side effects when building multiple targets.

Replace global configuration commands with their target-specific equivalents:
- Use `target_compile_definitions()` instead of `add_definitions()`
- Use `target_compile_options()` instead of setting `CMAKE_C_FLAGS`
- Use `target_include_directories()` instead of `include_directories()`

Example:
```cmake
# Avoid global settings
add_definitions(-D_POSIX_C_SOURCE=200112L -D_DEFAULT_SOURCE)
set(CMAKE_C_FLAGS "-O3 -Wall -Wextra -Wshadow")

# Prefer target-specific settings
target_compile_definitions(tree-sitter PRIVATE _POSIX_C_SOURCE=200112L _DEFAULT_SOURCE)
target_compile_options(tree-sitter PRIVATE -O3 -Wall -Wextra -Wshadow -Wno-unused-parameter -pedantic)
```

This approach ensures that configuration settings only apply to the intended targets and makes the build system more modular and predictable.