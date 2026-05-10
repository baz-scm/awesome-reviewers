---
title: Semantic Collision-Safe Naming
description: 'All identifiers should be (1) semantically clear, (2) consistent with
  project naming patterns, and (3) collision-safe.


  Apply this checklist:

  - Prefer clear, domain-meaningful names for configuration fields (avoid ambiguous
  terms like `resize_type` when the concept is “mode/sample_type”).'
repository: Tencent/ncnn
label: Naming Conventions
language: Other
comments_count: 5
repository_stars: 23205
---

All identifiers should be (1) semantically clear, (2) consistent with project naming patterns, and (3) collision-safe.

Apply this checklist:
- Prefer clear, domain-meaningful names for configuration fields (avoid ambiguous terms like `resize_type` when the concept is “mode/sample_type”).
  - Prefer names like `mode` / `sample_type` and keep comments consistent with the chosen name.
- For enum values, use explicit, scoped-like prefixes (especially when relying on C++11 enum scoping is optional).
  - Example:
    ```cpp
    enum InterpolationMode {
        Interpolation_BILINEAR = 1,
        Interpolation_Nearest = 2,
        Interpolation_BICUBIC = 3
    };
    ```
- Do not use leading underscore for member/attribute identifiers (e.g., avoid `int _axis`; use `int axis`).
- Avoid non-English transliterations (e.g., don’t introduce identifiers using Chinese Pinyin when an English/technical term exists).
- For macros/externally visible identifiers, always use project-qualified names to prevent collisions (e.g., replace `forceinline` with `NCNN_FORCE_INLINE`).

Result: names communicate intent, remain consistent across the codebase, and won’t conflict with external code or platform headers.