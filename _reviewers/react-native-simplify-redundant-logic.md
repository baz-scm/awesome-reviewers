---
title: simplify redundant logic
description: Eliminate redundant conditional logic, extract duplicated code, and choose
  simpler patterns over complex implementations. This improves code readability and
  maintainability by reducing cognitive load.
repository: facebook/react-native
label: Code Style
language: Other
comments_count: 7
repository_stars: 123178
---

Eliminate redundant conditional logic, extract duplicated code, and choose simpler patterns over complex implementations. This improves code readability and maintainability by reducing cognitive load.

Key practices:
- **Simplify redundant conditionals**: Instead of checking both directions of a condition, calculate once and use the result directly
- **Extract duplicated code**: When the same logic appears multiple times, extract it into a shared function or variable
- **Use existing properties**: Before creating new instance variables, check if existing properties can serve the same purpose
- **Avoid complex initialization patterns**: Prefer straightforward initialization in constructors over complex flag-based approaches
- **Choose simpler function designs**: Prefer return values over output parameters when possible

Example of simplifying redundant logic:
```cpp
// Instead of:
if (textHeight > lineHeight) {
    CGFloat difference = textHeight - lineHeight;
    verticalOffset = difference / 2.0;
} else if (textHeight < lineHeight) {
    CGFloat difference = lineHeight - textHeight;
    verticalOffset = -(difference / 2.0);
}

// Use:
CGFloat difference = textHeight - lineHeight;
CGFloat verticalOffset = difference / 2.0;
```

Example of using existing properties:
```cpp
// Instead of creating _initialProps, use existing _props:
if (_props) {
    // Use _props directly
}
```