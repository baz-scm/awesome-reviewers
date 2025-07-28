---
title: Target-aware configuration handling
description: When implementing features that depend on specific compilation targets
  or modes, design configuration mechanisms that gracefully handle target availability
  differences. Provide clear detection methods for feature availability on the current
  target, and ensure attributes and builtins work consistently across different compilation
  contexts.
repository: llvm/llvm-project
label: Configurations
language: Other
comments_count: 3
repository_stars: 33702
---

When implementing features that depend on specific compilation targets or modes, design configuration mechanisms that gracefully handle target availability differences. Provide clear detection methods for feature availability on the current target, and ensure attributes and builtins work consistently across different compilation contexts.

For heterogeneous compilations, distinguish between general feature availability and target-specific availability. Use `__has_target_builtin` for target-specific checks rather than `__has_builtin` when the actual code generation capability matters:

```cpp
#ifdef __CUDA__
#if __has_target_builtin(__builtin_trap)
  __builtin_trap();
#else
  abort();
#endif
#endif
```

For attributes that span multiple compilation modes, allow them to be present across all relevant targets even if they only affect specific ones. This enables consistent semantic analysis and diagnostics while maintaining target-specific behavior. For example, allow `sycl_external` on both host and device compilations to support unified diagnostic checking.

When target validation is complex or depends on build-time configuration, prefer graceful degradation over strict validation that could fail based on build flags. Treat target specifications as authoritative at the IR level and only validate what can be reliably checked without external dependencies.