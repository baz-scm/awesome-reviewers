---
title: Avoid breaking changes
description: When modifying existing APIs, prioritize backward compatibility to prevent
  breaking changes that would force developers to maintain separate code paths for
  different SDK versions. Use deprecation with clear migration paths instead of direct
  breaking changes, make new parameters optional with sensible defaults, and avoid
  changing existing default values.
repository: flutter/flutter
label: API
language: Other
comments_count: 5
repository_stars: 172252
---

When modifying existing APIs, prioritize backward compatibility to prevent breaking changes that would force developers to maintain separate code paths for different SDK versions. Use deprecation with clear migration paths instead of direct breaking changes, make new parameters optional with sensible defaults, and avoid changing existing default values.

For new required parameters, add them as optional with defaults:
```dart
// Instead of breaking change:
void getHandleAnchor(TextSelectionHandleType type, double textLineHeight, {required double cursorWidth})

// Use optional with default:
void getHandleAnchor(TextSelectionHandleType type, double textLineHeight, {double cursorWidth = 2.0})
```

For API replacements, use proper deprecation:
```dart
@Deprecated(
  'Use sendAnnouncement instead. '
  'This API is incompatible with multiple windows. '
  'This feature was deprecated after 3.35.0-0.1.pre.'
)
static Future<void> announce(String message) { ... }

static Future<void> sendAnnouncement(int viewId, String message) { ... }
```

Avoid changing default values as this constitutes a breaking change. Instead, add new options while preserving existing defaults. When designing new APIs, make parameters explicit rather than implicit to prevent future breaking changes when assumptions need to be updated.