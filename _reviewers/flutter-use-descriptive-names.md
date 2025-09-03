---
title: Use descriptive names
description: Names should clearly describe what they represent or do, rather than
  how they're implemented or using generic terms. Avoid abbreviations and use full,
  descriptive words that accurately reflect the purpose and behavior of the code element.
repository: flutter/flutter
label: Naming Conventions
language: Other
comments_count: 13
repository_stars: 172252
---

Names should clearly describe what they represent or do, rather than how they're implemented or using generic terms. Avoid abbreviations and use full, descriptive words that accurately reflect the purpose and behavior of the code element.

Key principles:
- Choose names that describe the actual purpose: `_scrollToFirstSelectableDate` instead of `_checkOnCustomDaysDisplay`
- Use full words instead of abbreviations: `lineHeightFactor` instead of `lineHeight`, avoid "hsw" for `half_stroke_width`
- Reflect the actual data type or behavior: `ExpectedFrameConstraints` instead of `ExpectedFrameSize` when returning constraints
- Use semantic accuracy over implementation details: `traversalOwner` instead of `overlayPortalParent` to avoid widget-layer concepts
- Follow language style guidelines: use `text_frame` in C++, avoid anonymous parameter names like `_`
- Apply conventional prefixes: `k` for constants (`kSystemToolbarToggleDebounceThreshold`), `handle` for callbacks (`handleSystemHideToolbar`)

Example of good descriptive naming:
```dart
// Bad: Generic and unclear purpose
void _checkOnCustomDaysDisplay() { ... }

// Good: Clearly describes what the function does
void _scrollToFirstSelectableDate() { ... }

// Bad: Abbreviation
final double hsw = half_stroke_width;

// Good: Full descriptive name
final double halfStrokeWidth = half_stroke_width;
```

This approach improves code readability and maintainability by making the codebase self-documenting through clear, purposeful naming.