---
title: Explain non-obvious code
description: Add explanatory comments for any code that isn't immediately self-explanatory,
  including magic numbers, implementation decisions, parameter purposes, and edge
  cases. This improves code maintainability and helps future developers understand
  the reasoning behind specific choices.
repository: flutter/flutter
label: Documentation
language: Other
comments_count: 15
repository_stars: 172252
---

Add explanatory comments for any code that isn't immediately self-explanatory, including magic numbers, implementation decisions, parameter purposes, and edge cases. This improves code maintainability and helps future developers understand the reasoning behind specific choices.

Key areas requiring explanation:
- **Magic numbers and constants**: Document how values were derived and their significance
- **Parameter relationships**: Explain dependencies, constraints, and edge case behavior  
- **Implementation decisions**: Clarify why specific approaches were chosen
- **Non-obvious logic**: Add context for complex conditional statements or calculations
- **Platform-specific behavior**: Document differences across platforms or versions

```dart
// Bad: No explanation for magic numbers or logic
class MaterialTextSelectionControls extends TextSelectionControls {
  @override
  Offset getHandleAnchor(TextSelectionHandleType type, double textLineHeight) {
    return switch (type) {
      TextSelectionHandleType.collapsed => const Offset(_kHandleSize / 2.18, -4.5),
      // ...
    };
  }
}

// Good: Clear explanations provided
class MaterialTextSelectionControls extends TextSelectionControls {
  @override
  Offset getHandleAnchor(TextSelectionHandleType type, double textLineHeight) {
    return switch (type) {
      // These values were eyeballed to match a physical Pixel 9 running Android 16,
      // which horizontally centers the anchor 1 pixel below the cursor.
      TextSelectionHandleType.collapsed => const Offset(_kHandleSize / 2.18, -4.5),
      // ...
    };
  }
}

// Bad: Unclear parameter purpose
void hideToolbar([bool hideHandles = true, Duration? toggleDebounceDuration]);

// Good: Parameter purpose documented
/// Hides the text selection toolbar.
///
/// By default, [hideHandles] is true, and the toolbar is hidden along with its
/// handles. If [hideHandles] is set to false, then the toolbar will be hidden
/// but the handles will remain.
///
/// When [toggleDebounceDuration] is non-null, a subsequent call to [toggleToolbar]
/// should not show the toolbar unless a duration threshold has been exceeded.
void hideToolbar([bool hideHandles = true, Duration? toggleDebounceDuration]);
```

This practice is especially important for Flutter framework code where implementation details affect developer experience and debugging.