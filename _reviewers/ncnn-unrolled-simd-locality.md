---
title: Unrolled SIMD Locality
description: 'When optimizing hot kernels (SIMD/vectorized paths), remove avoidable
  overhead and improve locality:


  1) Unroll small fixed-size tails (e.g., remainder=4)'
repository: Tencent/ncnn
label: Performance Optimization
language: C++
comments_count: 7
repository_stars: 23205
---

When optimizing hot kernels (SIMD/vectorized paths), remove avoidable overhead and improve locality:

1) Unroll small fixed-size tails (e.g., remainder=4)
- Replace remainder loops with straight-line stores/loads to eliminate loop counters and per-iteration branches.
- Example (tail of 4 elements with alternating sources):
```cpp
// Instead of: for (int i=0;i<4;i++){ if(i%2)... }
// Do a straight-line unroll:
{
    outptr[0] = ptr0[0];
    outptr[1] = ptr1[0];
    outptr[2] = ptr0[1];
    outptr[3] = ptr1[1];
    ptr0 += 2;
    ptr1 += 2;
    outptr += 4;
}
```

2) Use packed/contiguous intermediate buffers in vector code
- Prefer layouts that store multiple small fields (e.g., 4 lanes of coeffs/offsets) contiguously to reduce pointer chasing, TLB misses, and cache fragmentation.
- Example style:
```cpp
// Instead of separate small-dim Mats that increase pointer indirections,
// create a single contiguous layout:
offset_blob.create(outw, outh, elemsize * 4, 4, opt.workspace_allocator);
value_blob.create(outw, outh, elemsize * 2, 2, opt.workspace_allocator);
// (Or merge offset+value into one buffer when feasible.)
```

3) Keep ISA guards and branching structure “compiler-friendly”
- Use correct feature checks (don’t assume `__AVX2__` implies `__AVX__`):
  `#if defined(__AVX__) && defined(__AVX2__)`.
- Avoid placing `elempack==1` scalar handling inside SIMD-only macros in a way that blocks optimization; keep `elempack` branching clear at the appropriate scope.

4) For reductions, avoid inefficient reduction patterns
- Don’t perform costly “reduce” operations inside tight loops; restructure so reduction is done efficiently (e.g., accumulate vectors, then reduce once).

These rules target the same bottlenecks discussed: loop/branch overhead on tiny remainders, poor memory locality for intermediates, and avoidable SIMD/ISA/reduction inefficiencies.