---
title: avoid !! operator
description: Avoid using the not-null assertion operator (`!!`) as it can cause runtime
  crashes if the assumption about non-nullability is incorrect. Instead, use safer
  alternatives that provide better error handling and code clarity.
repository: facebook/react-native
label: Null Handling
language: Kotlin
comments_count: 7
repository_stars: 123178
---

Avoid using the not-null assertion operator (`!!`) as it can cause runtime crashes if the assumption about non-nullability is incorrect. Instead, use safer alternatives that provide better error handling and code clarity.

**Preferred alternatives:**

1. **Use `checkNotNull()` or `requireNotNull()`** for explicit null validation with meaningful error messages:
```kotlin
// Instead of:
drawable = draweeHolder.topLevelDrawable!!

// Use:
drawable = checkNotNull(draweeHolder.topLevelDrawable) { "Drawable should not be null" }
```

2. **Use Elvis operator (`?:`)** for providing fallback values or throwing exceptions:
```kotlin
// Instead of:
val local = instance().connectNative(pageId, remote)
local ?: throw IllegalStateException("Can't open failed connection")

// Use:
instance().connectNative(pageId, remote) ?: throw IllegalStateException("Can't open failed connection")
```

3. **Use smart casting with `is` checks** to avoid unnecessary null states:
```kotlin
// Instead of:
if (value !is Boolean) {
    throw ClassCastException("Dynamic value from Object is not a boolean")
}
return value as Boolean

// Use:
if (value is Boolean) {
    return value
}
throw ClassCastException("Dynamic value from Object is not a boolean")
```

The `!!` operator should only be used when you have absolute certainty that the value cannot be null, and even then, consider if a more explicit null check would make the code clearer and safer for future maintainers.