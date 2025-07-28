---
title: avoid Hungarian notation
description: Do not use Hungarian notation prefixes (like `m`, `s`) in variable and
  field names. Use descriptive, semantic names that clearly indicate the variable's
  purpose without encoding type or scope information in the name.
repository: facebook/react-native
label: Naming Conventions
language: Kotlin
comments_count: 5
repository_stars: 123178
---

Do not use Hungarian notation prefixes (like `m`, `s`) in variable and field names. Use descriptive, semantic names that clearly indicate the variable's purpose without encoding type or scope information in the name.

Hungarian notation makes code less readable and goes against Kotlin naming conventions. Instead of prefixing variables with their scope or type, choose names that describe what the variable represents.

**Examples:**

```kotlin
// ❌ Avoid Hungarian notation
private val mObject: Any? = null
private val sHelperRect: Rect = Rect()
public val mBackingMap: ReadableMap = props
private val mDecoder: CharsetDecoder = charset.newDecoder()

// ✅ Use semantic names
private val value: Any? = null
private val helperRect: Rect = Rect()
public val backingMap: ReadableMap = props
private val decoder: CharsetDecoder = charset.newDecoder()
```

This applies to all variable types including fields, parameters, and local variables. Focus on choosing names that communicate the variable's role and meaning in the context of your code.