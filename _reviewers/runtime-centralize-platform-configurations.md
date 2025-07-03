---
title: Centralize platform configurations
description: 'Platform-specific code and API usage should be centralized in designated
  configuration files rather than scattered throughout the codebase. When adding code
  that might not be available on all supported platforms:'
repository: dotnet/runtime
label: Configurations
language: C
comments_count: 2
repository_stars: 16578
---

Platform-specific code and API usage should be centralized in designated configuration files rather than scattered throughout the codebase. When adding code that might not be available on all supported platforms:

1. Use feature detection via CMake's `check_symbol_exists` or similar mechanisms
2. Define feature macros in a central configuration file
3. Use conditional compilation based on these macros
4. Consider adding polyfills for platforms missing specific APIs

For example, instead of embedding platform checks throughout your code:

```c
// Not recommended: platform-specific code scattered in implementation
void* SystemNative_AlignedAlloc(uintptr_t alignment, uintptr_t size)
{
#if defined(__APPLE__)
  // macOS-specific implementation
#elif defined(__linux__)
  // Linux-specific implementation
#endif
}

// Recommended: Use centralized feature detection
#include "pal_config.h" // Contains centrally defined HAVE_* macros

void* SystemNative_AlignedAlloc(uintptr_t alignment, uintptr_t size)
{
#if HAVE_ALIGNED_ALLOC
  return aligned_alloc(alignment, size);
#elif HAVE_POSIX_MEMALIGN
  void* result = NULL;
  return posix_memalign(&result, alignment, size) == 0 ? result : NULL;
#else
  // Fallback implementation for platforms without native support
  return malloc(size);
#endif
}
```

This approach improves maintainability, makes configuration audits easier, and centralizes knowledge about platform differences.
