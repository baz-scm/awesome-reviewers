---
title: Document complex logic
description: Add clear explanatory comments to complex calculations, platform-specific
  behavior, or non-obvious code sections. Use NOTE comments to explain the reasoning
  behind tricky implementations, especially when dealing with framework-specific quirks
  or mathematical calculations.
repository: facebook/yoga
label: Code Style
language: Objective-C
comments_count: 3
repository_stars: 18255
---

Add clear explanatory comments to complex calculations, platform-specific behavior, or non-obvious code sections. Use NOTE comments to explain the reasoning behind tricky implementations, especially when dealing with framework-specific quirks or mathematical calculations.

This practice improves code maintainability and helps other developers understand the rationale behind complex logic. Comments should explain the "why" rather than the "what", particularly for code that might seem counterintuitive or handles edge cases.

Example:
```objc
// NOTE: The center is offset by the layer.anchorPoint, so we have to take it into account.
view.center = (CGPoint) {
    .x = YGRoundPixelValue(x + (width * view.layer.anchorPoint.x)),
    .y = YGRoundPixelValue(y + (height * view.layer.anchorPoint.y)),
};

// NOTE: We must set only the bounds' size and keep the origin.
// UIScrollView's bounds.origin is not .zero when a contentOffset is set.
view.bounds = (CGRect) {
    .origin = view.bounds.origin,
    .size = {
        .width = YGRoundPixelValue(width),
        .height = YGRoundPixelValue(height),
    },
};
```