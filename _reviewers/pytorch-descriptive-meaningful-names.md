---
title: Descriptive meaningful names
description: Names should be clear, descriptive, and follow PyTorch's naming conventions.
  Variable names should precisely convey their purpose, avoiding ambiguity and shadowing.
  Boolean methods should use prefixes like `is_` or `has_` to indicate their nature.
repository: pytorch/pytorch
label: Naming Conventions
language: Other
comments_count: 5
repository_stars: 91169
---

Names should be clear, descriptive, and follow PyTorch's naming conventions. Variable names should precisely convey their purpose, avoiding ambiguity and shadowing. Boolean methods should use prefixes like `is_` or `has_` to indicate their nature.

Examples:
- ❌ `size_t t` → ✅ `size_t nodeIdx` or `size_t timeStep`
- ❌ `symm_mem()` → ✅ `is_symmetric()`
- ❌ `src` (shadowing) → ✅ `src_`

Always follow PyTorch's established naming conventions, avoiding camel case for variables. Properly named identifiers significantly improve code readability and maintainability, especially in open source contexts where many developers interact with the code.
