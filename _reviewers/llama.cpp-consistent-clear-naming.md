---
title: consistent clear naming
description: Ensure variable and identifier names are both consistent and unambiguous
  within their context. When multiple equivalent naming options exist (such as `tile_B::I`
  vs `tile_C::J` for the same value), choose one approach and apply it consistently
  throughout the codebase. Additionally, select names that clearly distinguish their
  purpose and avoid confusion with...
repository: ggml-org/llama.cpp
label: Naming Conventions
language: CUDA
comments_count: 2
repository_stars: 83559
---

Ensure variable and identifier names are both consistent and unambiguous within their context. When multiple equivalent naming options exist (such as `tile_B::I` vs `tile_C::J` for the same value), choose one approach and apply it consistently throughout the codebase. Additionally, select names that clearly distinguish their purpose and avoid confusion with similar concepts in the same scope.

For consistency: If `tile_C::J` is chosen over `tile_B::I`, use `tile_C::J` consistently in all related code locations.

For clarity: Instead of potentially confusing names like `ne01` that might be mistaken for byte offsets, use more descriptive alternatives like `s01` that clearly indicate their distinct purpose.

This approach prevents both inconsistent naming patterns and semantic confusion that can lead to bugs and reduced code maintainability.