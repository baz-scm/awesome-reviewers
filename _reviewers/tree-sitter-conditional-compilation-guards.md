---
title: Conditional compilation guards
description: Always use appropriate preprocessor directives to guard platform-specific,
  version-dependent, or feature-specific code. Ensure that conditional compilation
  checks accurately reflect the actual availability of features and APIs, not just
  version numbers or single configuration flags.
repository: tree-sitter/tree-sitter
label: Configurations
language: C
comments_count: 4
repository_stars: 21799
---

Always use appropriate preprocessor directives to guard platform-specific, version-dependent, or feature-specific code. Ensure that conditional compilation checks accurately reflect the actual availability of features and APIs, not just version numbers or single configuration flags.

When gating functionality:
- Use specific feature flags rather than generic version checks when possible
- Combine multiple conditions when a feature depends on both version AND configuration state
- Provide alternative implementations or graceful degradation for unsupported platforms
- Maintain consistency in feature flag naming and usage across the codebase

Example of proper conditional compilation:
```c
#ifdef TREE_SITTER_FEATURE_WASM
// WASM-specific code that requires __builtin_wasm_memory_size
#endif

#if PY_MINOR_VERSION >= 13 && !defined(Py_GIL_DISABLED)
{Py_mod_gil, Py_MOD_GIL_NOT_USED},
#endif

#elif !defined(__wasi__)
// Platform-specific implementation
#else
// WASI fallback or noop implementation
#endif
```

This prevents compilation errors across different environments and ensures code portability while maintaining feature availability where supported.