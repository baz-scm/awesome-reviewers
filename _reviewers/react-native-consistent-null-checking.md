---
title: consistent null checking
description: Ensure null checks follow consistent patterns and proper ordering for
  better readability and safety. Always place the variable being checked on the left
  side of null comparisons, use defensive programming with hasKey() checks before
  accessing map values, and maintain null-safe fallbacks when appropriate.
repository: facebook/react-native
label: Null Handling
language: Java
comments_count: 3
repository_stars: 123178
---

Ensure null checks follow consistent patterns and proper ordering for better readability and safety. Always place the variable being checked on the left side of null comparisons, use defensive programming with hasKey() checks before accessing map values, and maintain null-safe fallbacks when appropriate.

Key practices:
- Use `variable != null` instead of `null != variable` for better readability
- Implement defensive checks like `action.hasKey("key")` before accessing map values
- Consider null-safe fallbacks: `action.hasKey("label") ? action.getString("label") : null`
- Add explicit null checks for potentially nullable return values, even when parent objects are non-null

Example:
```java
// Good: Consistent ordering and defensive programming
if (!action.hasKey("name") || !action.hasKey("label")) {
  throw new IllegalArgumentException("Unknown accessibility action.");
}
String actionLabel = action.hasKey("label") ? action.getString("label") : null;

// Good: Proper null check ordering
if (!mSendMomentumEvents || mPostSmoothScrollRunnable != null) {
  return;
}

// Avoid: Inconsistent null check ordering
if (!mSendMomentumEvents || null != mPostSmoothScrollRunnable) {
  return;
}
```