---
title: Leverage Kotlin null-safety
description: 'Utilize Kotlin''s null-safety features effectively to create cleaner,
  more robust code:


  1. For class properties that will be initialized before use, prefer `lateinit var`
  over nullable types with `?`:'
repository: spring-projects/spring-framework
label: Null Handling
language: Kotlin
comments_count: 3
repository_stars: 58382
---

Utilize Kotlin's null-safety features effectively to create cleaner, more robust code:

1. For class properties that will be initialized before use, prefer `lateinit var` over nullable types with `?`:
```kotlin
// Avoid
private var server: MockWebServer? = null

// Prefer
private lateinit var server: MockWebServer
```

2. Design API signatures to minimize forcing clients to use the unsafe `!!` operator:
```kotlin
// Avoid
suspend fun <T : Any> TransactionalOperator.executeAndAwait(f: suspend (ReactiveTransaction) -> T?): T?

// Prefer
suspend fun <T> TransactionalOperator.executeAndAwait(f: suspend (ReactiveTransaction) -> T): T
```

3. Avoid redundant null checks when Kotlin's null-safety operators are already in use:
```kotlin
// Redundant
val ctor = BeanUtils.findPrimaryConstructor(SomeClass::class.java)!!
assertThat(ctor).isNotNull() // Unnecessary since !! already asserts non-null

// Cleaner
val ctor = BeanUtils.findPrimaryConstructor(SomeClass::class.java)!!
// Continue using ctor directly
```