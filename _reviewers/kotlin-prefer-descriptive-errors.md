---
title: Prefer descriptive errors
description: When handling errors in your code, always provide detailed context in
  error messages to aid debugging. Use Kotlin's standard error handling functions
  instead of directly throwing exceptions or using non-null assertions.
repository: JetBrains/kotlin
label: Error Handling
language: Kotlin
comments_count: 6
repository_stars: 50857
---

When handling errors in your code, always provide detailed context in error messages to aid debugging. Use Kotlin's standard error handling functions instead of directly throwing exceptions or using non-null assertions.

1. Use `error()` function with descriptive messages instead of throwing exceptions directly:
```kotlin
// Bad
if (companion.isCompanion == false) {
    throw AssertionError() // Unhelpful message
}

// Good
if (companion.isCompanion == false) {
    error("Expected $companion to be a companion object")
}
```

2. When reporting errors from caught exceptions, preserve cause information:
```kotlin
// Bad
catch (e: IllegalStateException) {
    reportError(e.message!!)
    throw CompilationErrorException()
}

// Good
catch (e: IllegalStateException) {
    reportError("${e.message}\nCaused by: ${e.cause?.javaClass?.name}: ${e.cause?.message}")
    throw CompilationErrorException()
}
```

3. Use null-safe operators with descriptive error messages instead of non-null assertions:
```kotlin
// Bad
val fieldName = getterCall.symbol.owner.name.getFieldName()!!

// Good
val fieldName = getterCall.symbol.owner.name.getFieldName() 
    ?: error("Expected getter call to have a field name")
```

4. Include relevant context in assertion messages:
```kotlin
// Bad
assert(companion.isCompanion)

// Good
assert(companion.isCompanion) { "Expected $companion to be a companion object" }
```

By following these practices, you'll make your code more maintainable and debugging much easier when errors inevitably occur.
