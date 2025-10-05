---
title: Safe configuration definitions
description: When defining configuration flags and options, use practices that ensure
  compatibility across different preprocessors and build environments. For macro-based
  configuration flags, use integer values (0/1) instead of boolean literals (true/false)
  to avoid preprocessor compatibility issues. Additionally, consider using runtime
  configuration mechanisms (like...
repository: facebook/yoga
label: Configurations
language: C++
comments_count: 2
repository_stars: 18255
---

When defining configuration flags and options, use practices that ensure compatibility across different preprocessors and build environments. For macro-based configuration flags, use integer values (0/1) instead of boolean literals (true/false) to avoid preprocessor compatibility issues. Additionally, consider using runtime configuration mechanisms (like config objects or flags) instead of compile-time options when flexibility is needed.

Example of safer macro definitions:
```cpp
// Safer - use integer values
#define PRINT_CHANGES 0
#define PRINT_SKIPS 0

// Or use properly defined constants
#define PRINT_CHANGES FALSE  // where FALSE is defined as 0

// Instead of potentially problematic boolean literals
#define PRINT_CHANGES false  // may cause preprocessor issues
```

For configuration mechanisms, prefer runtime configuration over compile-time when possible:
```cpp
// Better - runtime configuration via config object
YGConfig config;
config.callMeasureCallbackOnAllNodes = true;

// Instead of compile-time only
#ifdef YOGA_CALL_MEASURE_CALLBACK_ON_ALL_NODES
```

This approach ensures better portability across different compilers and preprocessors while providing more flexibility for users of your code.