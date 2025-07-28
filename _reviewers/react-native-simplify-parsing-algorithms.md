---
title: Simplify parsing algorithms
description: When implementing parsing or processing algorithms, prioritize simplification
  and reusability over complex custom solutions. Convert complex conditional logic
  into simpler, well-defined data structures and reusable functions. Use established,
  proven algorithms from reliable sources rather than deriving custom implementations.
repository: facebook/react-native
label: Algorithms
language: JavaScript
comments_count: 3
repository_stars: 123178
---

When implementing parsing or processing algorithms, prioritize simplification and reusability over complex custom solutions. Convert complex conditional logic into simpler, well-defined data structures and reusable functions. Use established, proven algorithms from reliable sources rather than deriving custom implementations.

For example, instead of complex nested conditionals for parsing gradient directions:
```javascript
// Before: Complex conditional parsing
if (typeof bgImage.direction === 'undefined') {
  points = TO_BOTTOM_START_END_POINTS;
} else if (ANGLE_UNIT_REGEX.test(bgImage.direction)) {
  const angle = parseAngle(bgImage.direction);
  if (angle != null) {
    points = calculateStartEndPointsFromAngle(angle);
  }
} else if (DIRECTION_REGEX.test(bgImage.direction)) {
  // More complex logic...
}

// After: Simplified with reusable orientation structure
let orientation: LinearGradientOrientation = DEFAULT_ORIENTATION;
if (bgImage.direction != null && ANGLE_UNIT_REGEX.test(bgImage.direction)) {
  const parsedAngle = getAngleInDegrees(bgImage.direction);
  if (parsedAngle != null) {
    orientation = { type: 'angle', value: parsedAngle };
  }
}
```

This approach makes algorithms more maintainable, testable, and allows for better code reuse across different parts of the system. When dealing with complex patterns like URL validation, prefer established regex patterns from trusted sources over custom derivations.