---
title: Avoid Performance Pessimization
description: When optimizing for CPU/GPU speed, don’t accidentally remove fast paths
  via build/toolchain settings, and don’t add expensive memory-access patterns in
  the hottest kernels.
repository: Tencent/ncnn
label: Performance Optimization
language: Other
comments_count: 5
repository_stars: 23205
---

When optimizing for CPU/GPU speed, don’t accidentally remove fast paths via build/toolchain settings, and don’t add expensive memory-access patterns in the hottest kernels.

Apply this standard:
1) Don’t globally disable ISA features or runtime CPU dispatch from generic toolchain files
- Only apply ISA restrictions for the specific target (e.g., legacy OS/CPU) and keep that list explicitly documented.
- Don’t redundantly set every descendant ISA knob when disabling a parent already covers it.
- Be aware that disabling runtime CPU dispatch can eliminate optimized code paths (e.g., xop) even when the target CPU supports them.

2) In SIMD kernels, avoid unnecessary gather/indirection for contiguous data
- If the source elements are contiguous, use normal vector loads (e.g., loadu/storeu) rather than gather instructions.
- Gather is for irregular/index-driven access; using it “just to mask” typically wastes bandwidth/latency.

3) Keep SIMD tail handling simple and width-driven
- Prefer clear “main loop + remainder” loops by SIMD width over complex `nn`/offset-tail bookkeeping.

4) Don’t assume `#pragma omp simd` will outperform hand-written intrinsics in hot paths
- For critical x86 kernels that already use explicit intrinsics, extra pragmas usually add complexity with minimal speedup.

Example (contiguous access vs gather):
```cpp
// Bad: gather when srcptr is contiguous and offsets are sequential
// __m256 v00_val = mask_gather_ps256(srcptr, v00_offset, mask);

// Good: use vector load directly when indices are contiguous
// (illustrative; exact mask logic depends on bounds)
__m256 v00_val = _mm256_loadu_ps(srcptr + base_index);
// apply mask/lerp/fma as needed
```

Example (width-driven tail loop instead of nn bookkeeping):
```cpp
int x = 0;
#if __SSE2__
#if __AVX__
for (; x + 7 < grid_size; x += 8) {
    // AVX body
}
#endif
for (; x + 3 < grid_size; x += 4) {
    // SSE body
}
#endif
for (; x < grid_size; x++) {
    // scalar remainder
}
```

Net effect: you preserve the compiler/runtime ability to select the fastest supported implementation, and you prevent common “hidden” slowdowns from gather/indirection and overly complex SIMD tails.