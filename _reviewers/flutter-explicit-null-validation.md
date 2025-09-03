---
title: explicit null validation
description: Always validate null values explicitly rather than using silent fallbacks
  or implicit handling. When null values are unexpected or could cause issues, use
  assertions or explicit checks to fail fast and provide clear error messages.
repository: flutter/flutter
label: Null Handling
language: Other
comments_count: 6
repository_stars: 172252
---

Always validate null values explicitly rather than using silent fallbacks or implicit handling. When null values are unexpected or could cause issues, use assertions or explicit checks to fail fast and provide clear error messages.

Avoid silent fallbacks like `DateTime.now()` when a null value indicates a programming error. Instead, use explicit null checks and assertions to catch issues early in development.

**Prefer explicit validation:**
```dart
// Bad - silent fallback
selectableDayPredicate?.call(initialDateTime ?? DateTime.now())

// Good - explicit null handling  
assert(
  selectableDayPredicate == null || 
  initialDate == null || 
  selectableDayPredicate!(initialDate!),
  'Initial date must be selectable when predicate is provided'
);
```

**Use assertions for unexpected nulls:**
```dart
// Bad - silent failure
final VoidCallback? callback = callbacks[actionId];
if (callback != null) {
  callback();
}

// Good - explicit validation
final VoidCallback? callback = callbacks[actionId];
assert(callback != null, 'No callback registered for action: $actionId');
callback?.call();
```

**Validate numeric values:**
```dart
// Bad - silent failure on invalid values
if (itemExtent > 0.0) {
  // process...
}

// Good - explicit validation
if (itemExtent > 0.0 && scrollOffset.isFinite && itemExtent.isFinite) {
  // process...
} else {
  assert(false, 'Invalid numeric values: itemExtent=$itemExtent, scrollOffset=$scrollOffset');
}
```

This approach prevents crashes from unexpected null values, makes debugging easier by failing fast with clear messages, and ensures that null handling is intentional rather than accidental.