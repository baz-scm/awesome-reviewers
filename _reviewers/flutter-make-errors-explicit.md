---
title: Make errors explicit
description: Always make error conditions explicit and visible rather than hiding
  them through silent failures, default return values, or unchecked operations. This
  includes validating results before use, using assertions for invalid states, and
  logging unexpected conditions.
repository: flutter/flutter
label: Error Handling
language: Other
comments_count: 4
repository_stars: 172252
---

Always make error conditions explicit and visible rather than hiding them through silent failures, default return values, or unchecked operations. This includes validating results before use, using assertions for invalid states, and logging unexpected conditions.

Key practices:
- Check results of operations like `find()` before dereferencing to prevent crashes
- Use assertions instead of returning default values to hide errors: `assert(scrollOffset.isFinite && itemExtent.isFinite)` rather than `return 0`
- Add error logging for conditions that shouldn't happen: `FML_LOG(ERROR) << "Unexpected condition"`
- Throw clear errors for unexpected duplicate events rather than silently ignoring them

Example of making errors explicit:
```dart
// Bad: Hides error by returning default value
if (itemExtent > 0.0) {
  final double actual = scrollOffset / itemExtent;
  if (!actual.isFinite) {
    return 0; // Silently hides the error
  }
}

// Good: Makes error explicit with assertion
assert(scrollOffset.isFinite && itemExtent.isFinite, 
       'scrollOffset and itemExtent must be finite');
if (itemExtent > 0.0) {
  final double actual = scrollOffset / itemExtent;
}
```

This approach helps developers identify issues during development and provides better debugging information when problems occur.