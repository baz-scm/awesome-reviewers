---
title: Capability-Guarded Configuration
description: When code depends on environment/build features (SIMD/FP16 availability,
  OpenCV versioned APIs, packing layout support, OS/ABI-specific macros), you must
  (1) gate the code at compile time with the correct macros and (2) reflect the real
  capability in the backend’s `support_*` flags so the framework won’t select an unsupported
  execution path.
repository: Tencent/ncnn
label: Configurations
language: C++
comments_count: 6
repository_stars: 23205
---

When code depends on environment/build features (SIMD/FP16 availability, OpenCV versioned APIs, packing layout support, OS/ABI-specific macros), you must (1) gate the code at compile time with the correct macros and (2) reflect the real capability in the backend’s `support_*` flags so the framework won’t select an unsupported execution path.

Apply this as a standard checklist:
- Optional dependencies: wrap includes/usages in the correct version guards (e.g., `CV_MAJOR_VERSION`/`CV_MINOR_VERSION`).
- SIMD/FP16 paths: guard the *whole* implementation and call sites with the precise feature expression (e.g., NEON + the required FP mode), not only `__ARM_NEON`.
- Backend packing/layout: if a packing layout or axis is not implemented, disable it in `create_pipeline()` (e.g., set `support_packing = false` or the equivalent packing flags), and then you can remove/avoid unused unpacking glue.
- OS/arch macros: prefer correct architecture detection macros for each platform target (e.g., consider `_WIN32` when detecting x64).

Example patterns:
```cpp
// 1) Version-gated optional headers
#if (CV_MAJOR_VERSION >= 3)
#include <opencv2/videoio/videoio.hpp>
#endif

// 2) SIMD/FP16 gated implementation
#if defined(__ARM_NEON) && (__ARM_FP & 2)
static int lstm_fp16(...){ /* fp16 NEON path */ }
#endif

// 3) Capability flags match implementation
int InnerProduct_arm::create_pipeline(const Option& opt)
{
    if (axis == 1)
        support_packing = false; // packing/layout not implemented for this axis
    return 0;
}

// 4) If you disable packing support, don’t keep unpacking logic around
if (!support_vulkan_packing && !support_vulkan_any_packing)
{
    // avoid selecting unpack/convert glue; only accept supported layouts
}
```

This prevents build-breaks on unsupported platforms, avoids dead/incorrect code paths, and ensures runtime execution matches what the backend actually supports.