---
title: Consistency And Readability
description: 'Apply a single, repeatable style checklist across all new/modified code:


  1) Remove unused/redundant code

  - Drop unused `#include`s and unused variables.'
repository: Tencent/ncnn
label: Code Style
language: C++
comments_count: 14
repository_stars: 23205
---

Apply a single, repeatable style checklist across all new/modified code:

1) Remove unused/redundant code
- Drop unused `#include`s and unused variables.
- Don’t add overrides or plumbing that the base class already provides (avoid “override without purpose”).
- Keep diffs focused: avoid unrelated call-site churn when a helper can encapsulate logic.

2) Keep compiler/standard compatibility
- Don’t use C++11-only syntax where the project targets older compilers/standards (e.g., avoid `{...}` initializer lists).
- Avoid range-based `for` if the codebase/toolchain constraints require explicit indexing.
- For const objects, ensure initialization is explicitly safe for older clangs (prefer `const T t = {};` over uninitialized default construction).

3) Factor preprocessor/SIMD-heavy logic for readability
- When you have long `#if/#ifdef` blocks for SSE/AVX/AVX512, move the implementation into small helper functions (e.g., `packA_*`, `packB_*`, `subkernel_*`) so the main algorithm focuses on tiling/control flow.

4) Enforce formatting conventions
- Use consistent comment formatting (UTF-8, `// comment` with a space; keep meaningful text aligned with code).
- Prefer correct preprocessor directives (`#if` vs `#ifdef`) and consistent patterns.
- Handle unused parameters cleanly (e.g., `(void)opt;`).

Example (SIMD factoring)
```cpp
static void packA_sse(const float* src, float* dst, int k, const Option& opt);
static void packA_avx(const float* src, float* dst, int k, const Option& opt);

for (int i = 0; i < M; i += TILE_M)
{
    // keep tiling/control logic here
    if (j == 0)
    {
#if __SSE2__
#if __AVX__
        packA_avx(A_ptr, AT_ptr, k, opt);
#else
        packA_sse(A_ptr, AT_ptr, k, opt);
#endif
#endif
    }
}
```