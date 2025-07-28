---
title: Use Kotlin testing idioms
description: When writing tests in Kotlin, prefer Kotlin-specific testing libraries
  and language features over their Java equivalents. Use Mockito Kotlin instead of
  standard Mockito for more idiomatic syntax, and leverage Kotlin language features
  like `apply` blocks to make test setup code more concise and readable.
repository: facebook/react-native
label: Testing
language: Kotlin
comments_count: 2
repository_stars: 123178
---

When writing tests in Kotlin, prefer Kotlin-specific testing libraries and language features over their Java equivalents. Use Mockito Kotlin instead of standard Mockito for more idiomatic syntax, and leverage Kotlin language features like `apply` blocks to make test setup code more concise and readable.

For example, instead of:
```kotlin
import org.mockito.Mockito.verify
// ...
val field = OkHttpClientProvider::class.java.getDeclaredField("sClient")
field.isAccessible = true
field.set(null, null)
```

Use:
```kotlin
import org.mockito.kotlin.verify
// ...
val field = OkHttpClientProvider::class.java.getDeclaredField("sClient").apply {
  isAccessible = true
  set(null, null)
}
```

This approach improves test code readability, reduces boilerplate, and takes advantage of Kotlin's expressive syntax to make tests more maintainable.