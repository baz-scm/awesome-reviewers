---
title: Use nullish coalescing
description: When providing default values for numeric properties, use the nullish
  coalescing operator (??) instead of logical OR (||). This ensures that valid zero
  values are preserved rather than being replaced with defaults. Using || will treat
  0 as a falsy value and replace it with the default, which is often unintended behavior
  for numeric settings.
repository: RooCodeInc/Roo-Code
label: Null Handling
language: TSX
comments_count: 3
repository_stars: 17288
---

When providing default values for numeric properties, use the nullish coalescing operator (??) instead of logical OR (||). This ensures that valid zero values are preserved rather than being replaced with defaults. Using || will treat 0 as a falsy value and replace it with the default, which is often unintended behavior for numeric settings.

This pattern is especially important for numeric configurations like thresholds, ranges, and input values where zero is a valid and meaningful value that should not be overridden.
