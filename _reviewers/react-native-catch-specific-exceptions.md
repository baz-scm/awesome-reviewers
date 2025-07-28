---
title: catch specific exceptions
description: Always catch specific exception types rather than generic `Exception`
  to avoid masking unexpected errors and ensure intentional error handling. This practice
  helps distinguish between expected failure scenarios that should be handled gracefully
  and unexpected errors that indicate bugs.
repository: facebook/react-native
label: Error Handling
language: Kotlin
comments_count: 3
repository_stars: 123178
---

Always catch specific exception types rather than generic `Exception` to avoid masking unexpected errors and ensure intentional error handling. This practice helps distinguish between expected failure scenarios that should be handled gracefully and unexpected errors that indicate bugs.

When handling known failure cases, catch the specific exception type that the API contract specifies. For example, when setting font variation settings which throws `IllegalArgumentException` for invalid input, catch only that specific exception:

```kotlin
try {
    fontVariationSettings = fontVariationSettingsParam
} catch (e: IllegalArgumentException) {
    Log.w(TAG, "Invalid font variation settings: $fontVariationSettingsParam", e)
    // Handle gracefully - continue without font variations
}
```

Avoid generic exception catching which can hide programming errors:
```kotlin
// DON'T DO THIS - masks all errors including unexpected ones
try {
    fontVariationSettings = fontVariationSettingsParam
} catch (e: Exception) {
    // This could hide NullPointerException, OutOfMemoryError, etc.
}
```

Additionally, validate inputs early to prevent crashes from edge cases, and remove unnecessary try blocks that have no catch or finally clauses as they create misleading code structure without providing error handling benefits.