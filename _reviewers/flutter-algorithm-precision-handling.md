---
title: Algorithm precision handling
description: 'Choose algorithms that handle edge cases and mathematical precision
  correctly to avoid subtle bugs and unexpected behavior.


  When implementing algorithms, prioritize mathematical soundness and robust edge
  case handling over apparent simplicity. Use established mathematical formulas and
  precise operations rather than approximations that may fail in corner...'
repository: flutter/flutter
label: Algorithms
language: Other
comments_count: 6
repository_stars: 172252
---

Choose algorithms that handle edge cases and mathematical precision correctly to avoid subtle bugs and unexpected behavior.

When implementing algorithms, prioritize mathematical soundness and robust edge case handling over apparent simplicity. Use established mathematical formulas and precise operations rather than approximations that may fail in corner cases.

**Key practices:**
- Use `substring()` instead of `split()` for string processing when you need precise control: `currentLabel.substring(baseLabel.length)` avoids issues when the base pattern appears multiple times
- Apply proper unit conversions with mathematical constants: `event.rotation = (double)state->rotation * (M_PI / 180)` for degrees to radians
- Handle floating-point precision in division operations: use `lerpValue.round()` after render-level calculations rather than redundant division-based rounding
- Validate all edge cases in algorithms, especially zero values and boundary conditions: check for `metrics.physical_width == 0` and constraint relationships
- Fix mathematical formulas to use correct operations: `(math.max(first.bottom, second.bottom) - math.min(first.top, second.top))` for proper area calculations

The goal is to prevent runtime failures and visual glitches caused by algorithmic edge cases that surface only under specific conditions. Invest time in understanding the mathematical properties of your algorithms and test boundary conditions thoroughly.