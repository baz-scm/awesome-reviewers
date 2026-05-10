---
title: Stable Public API Surface
description: When modifying or adding exported interfaces in public headers, ensure
  the external API surface is stable, easy to use across platforms/languages, and
  does not leak internal implementation details.
repository: Tencent/ncnn
label: API
language: Other
comments_count: 5
repository_stars: 23205
---

When modifying or adding exported interfaces in public headers, ensure the external API surface is stable, easy to use across platforms/languages, and does not leak internal implementation details.

Apply these rules:
1) Platform-agnostic signatures: wrap OS/platform-specific details inside internal types/modules; the public API should not force callers to use different types/macros per platform.
   - Example pattern:
   ```cpp
   // public header
   class CpuSet;
   CpuSet get_cpu_thread_affinity_mask(int powersave);
   ```
2) Consistent return types and lifetimes: prefer references to global/static data when the lifetime is guaranteed.
   - Example pattern:
   ```cpp
   // if the underlying object is always alive
   const CpuSet& get_cpu_thread_affinity_mask(int powersave);
   ```
3) Integration-friendly API design: when there is an established de-facto API (e.g., OpenCV), prefer compatibility in names/semantics so drop-in usage is possible.
4) Public header encapsulation: do not expose internal helper/holder classes or implementation-only types in public headers—move them to source files or internal headers.
5) Cross-language linkage: for functions meant to be called from C/other languages, guard declarations and definitions with `extern "C"` under `__cplusplus`.
   - Example pattern:
   ```cpp
   #ifdef __cplusplus
   extern "C" {
   #endif
   void some_exported_c_function(void);
   #ifdef __cplusplus
   }
   #endif
   ```

Outcome: callers get one predictable API surface regardless of platform, language, or internal refactors—reducing integration breakage and preventing accidental exposure of internal implementation details.