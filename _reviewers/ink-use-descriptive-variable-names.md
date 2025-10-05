---
title: Use descriptive variable names
description: Avoid single-character variables and abbreviations in favor of descriptive,
  full-word names that clearly communicate the variable's purpose or content. This
  improves code readability and makes the codebase more maintainable for other developers.
repository: vadimdemedes/ink
label: Naming Conventions
language: TSX
comments_count: 3
repository_stars: 31825
---

Avoid single-character variables and abbreviations in favor of descriptive, full-word names that clearly communicate the variable's purpose or content. This improves code readability and makes the codebase more maintainable for other developers.

Examples of improvements:
- Change `x` to `children` in function parameters
- Change `str` to `string` for string parameters  
- Change `e` to `focusable` when iterating over focusable elements

Descriptive names act as inline documentation, making code self-explanatory and reducing the cognitive load for developers reading or maintaining the code.