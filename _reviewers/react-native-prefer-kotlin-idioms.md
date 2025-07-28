---
title: prefer Kotlin idioms
description: Use Kotlin-specific constructs and syntax patterns instead of Java-style
  code to improve readability and maintainability. This includes leveraging Kotlin's
  expressive syntax features and standard library functions.
repository: facebook/react-native
label: Code Style
language: Kotlin
comments_count: 9
repository_stars: 123178
---

Use Kotlin-specific constructs and syntax patterns instead of Java-style code to improve readability and maintainability. This includes leveraging Kotlin's expressive syntax features and standard library functions.

Key practices to follow:

**Expression body syntax for simple functions:**
```kotlin
// Instead of
override fun contentType(): MediaType? {
    return responseBody.contentType()
}

// Use
override fun contentType(): MediaType? = responseBody.contentType()
```

**Kotlin collection builders:**
```kotlin
// Instead of
ArrayList<JavaModuleWrapper>().apply { ... }

// Use
buildList { ... } or mutableListOf()
```

**When expressions for complex conditionals:**
```kotlin
// Instead of multiple if-else chains
return when (value) {
    null -> ReadableType.Null
    is Boolean -> ReadableType.Boolean
    is Number -> ReadableType.Number
    else -> ReadableType.Null
}
```

**Properties over getter methods:**
```kotlin
// Instead of
fun getLifecycleState(): LifecycleState = state

// Use
val lifecycleState: LifecycleState
    get() = state
```

**Functional interfaces:**
```kotlin
// Use fun interface to enable lambda syntax
public fun interface BatchEventDispatchedListener {
    fun onBatchEventDispatched()
}
```

**Kotlin string builders:**
```kotlin
// Instead of StringBuilder
// Use
buildString { ... }
```

These patterns make code more concise, readable, and leverage Kotlin's strengths while reducing boilerplate compared to Java-style implementations.