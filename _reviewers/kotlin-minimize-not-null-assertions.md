---
title: Minimize not-null assertions
description: 'Avoid using not-null assertions (`!!`) when safer alternatives exist.
  Instead:

  1. Use safe calls (`?.`) when accessing properties or methods on nullable references'
repository: JetBrains/kotlin
label: Null Handling
language: Java
comments_count: 2
repository_stars: 50857
---

Avoid using not-null assertions (`!!`) when safer alternatives exist. Instead:
1. Use safe calls (`?.`) when accessing properties or methods on nullable references
2. Use the elvis operator (`?:`) to provide default values
3. Implement early returns with explicit null checks when appropriate

For example, instead of:
```kotlin
val result = nullableValue!!.doSomething()
```

Prefer:
```kotlin
// Safe call with elvis operator
val result = nullableValue?.doSomething() ?: defaultValue

// Or early return with null check
if (nullableValue == null) {
    return defaultValue // or handle the null case appropriately
}
val result = nullableValue.doSomething()
```

This pattern reduces the risk of NullPointerExceptions and makes code more robust. When reviewing code, look for unnecessary not-null assertions that could be replaced with safer constructs, as shown in the `UnnecessaryNotNullAssertionFix` class. Additionally, follow the pattern seen in the expression typing code where early returns are used when a descriptor is null.
