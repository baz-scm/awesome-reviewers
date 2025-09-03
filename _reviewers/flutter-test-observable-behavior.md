---
title: Test observable behavior
description: Focus on testing what users see and experience rather than internal implementation
  details. Tests should verify the actual behavior that matters to users, not how
  the code achieves that behavior internally.
repository: flutter/flutter
label: Testing
language: Other
comments_count: 4
repository_stars: 172252
---

Focus on testing what users see and experience rather than internal implementation details. Tests should verify the actual behavior that matters to users, not how the code achieves that behavior internally.

**Why this matters:**
- Tests remain valid when implementation changes
- Avoids the need for `@visibleForTesting` annotations
- Creates more maintainable and meaningful tests
- Catches real bugs that affect user experience

**Instead of testing implementation details:**
```dart
// Bad: Testing controller value directly
expect(controller.value, closeTo(0.5, 0.01));

// Bad: Adding @visibleForTesting just for tests
@visibleForTesting
Set<Color> distinctVisibleOuterColors() { ... }
```

**Test observable behavior:**
```dart
// Good: Test what the user sees - the actual progress indicator rendering
expect(
  find.byType(LinearProgressIndicator),
  paints
    ..rect(rect: expectedBackgroundRect)
    ..rect(rect: expectedProgressRect)
);

// Good: Test animation effects users can observe
expect(
  find.byType(FadeTransition),
  paints..opacity(0.5) // Test the actual fade effect
);
```

**Key practices:**
- Test visual output using `paints` matchers
- Verify user interactions and their effects
- Test accessibility announcements and semantic properties  
- Use existing public APIs to access test state
- Mock platform channels to test system integrations

This approach creates tests that are both more robust and more meaningful, as they verify the actual user experience rather than internal code structure.