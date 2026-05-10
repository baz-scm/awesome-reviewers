---
title: Use exact math semantics
description: 'When implementing performance-critical algorithms (e.g., pooling, math
  kernels, SIMD/ISA code), preserve the algorithm’s true numeric semantics and parameterization:'
repository: Tencent/ncnn
label: Algorithms
language: Other
comments_count: 2
repository_stars: 23205
---

When implementing performance-critical algorithms (e.g., pooling, math kernels, SIMD/ISA code), preserve the algorithm’s true numeric semantics and parameterization:

1) Match rounding/truncation semantics with the ISA’s exact instruction
- Prefer the native intrinsic that implements the intended operation (e.g., truncation toward zero) rather than approximating via integer conversion that may differ.
- Example (aarch64):
```cpp
static inline float32x4_t trunc_ps(const float32x4_t& x)
{
#if __aarch64__
    return vrndq_f32(x); // trunc toward zero
#else
    // fallback, but verify it matches trunc-toward-zero semantics
    int32x4_t xi = vcvtq_s32_f32(x);
    return vcvtq_f32_s32(xi);
#endif
}
```

2) Don’t “constant-fold” parameters that are mathematically location-dependent
- If kernel extents (or other algorithm parameters) vary per output position, compute them per position in the same execution space (shader/CPU) or pass the per-position values explicitly.
- For adaptive pooling: kernel_w/kernel_h generally depend on gx/gy (output location), so computing a single constant kernel on CPU and reusing it is incorrect. Keep the dynamic computation consistent with the reference definitions.

3) Add a quick correctness checklist during review
- Numeric ops: confirm rounding direction (floor/ceil/trunc) and tie behavior where relevant.
- Parameter definition: confirm which variables are constant vs per-location/per-channel.
- Kernel wiring: verify parameter order (e.g., bias vs kernel) to avoid silent swaps that still compile.

Applying this standard prevents cross-architecture drift (wrong rounding) and algorithm drift (wrong kernel sizes), which are frequent root causes of subtle accuracy regressions in algorithmic code paths.