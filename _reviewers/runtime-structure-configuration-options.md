---
title: Structure configuration options
description: Design and document configuration options (feature flags, environment
  variables, conditional compilation) to be clear, consistent, and maintainable. Group
  related configurations together and avoid unnecessary splits or redundancies. Document
  the purpose and behavior of each option, including valid values and interaction
  effects.
repository: dotnet/runtime
label: Configurations
language: C++
comments_count: 4
repository_stars: 16578
---

Design and document configuration options (feature flags, environment variables, conditional compilation) to be clear, consistent, and maintainable. Group related configurations together and avoid unnecessary splits or redundancies. Document the purpose and behavior of each option, including valid values and interaction effects.

For conditional compilation:
```cpp
// GOOD: Clear hierarchy and purpose
#if !defined(DACCESS_COMPILE) && !defined(FEATURE_CDAC_UNWINDER)
// Code for in-process execution only
#endif

// AVOID: Redundant or overly specific conditions
#if defined(HOST_WINDOWS) // Redundant if file is Windows-only
// ...
#endif
```

For environment variables, provide clear levels with documented behavior:
```cpp
// GOOD: Well-documented configuration with clear levels
// DOTNET_InterpreterMode=0: default, interpreter only used with explicit opt-in
// DOTNET_InterpreterMode=1: use interpreter except for R2R code and System.Private.CoreLib
// DOTNET_InterpreterMode=2: use interpreter for everything except intrinsics
// DOTNET_InterpreterMode=3: full interpreter-only mode, no fallbacks
```

For feature flags, consolidate related functionality until there's a clear need for separation:
```cpp
// PREFER: Single feature flag for closely related functionality
#ifdef FEATURE_JAVAMARSHAL
// All Java interop code including GC bridge
#endif

// AVOID: Premature separation that creates confusing boundaries
#ifdef FEATURE_JAVAMARSHAL
// Some Java interop code
#endif
#ifdef FEATURE_GCBRIDGE
// Closely related GC bridge functionality
#endif
```
