---
title: Test edge cases
description: Ensure tests verify both basic functionality and edge cases. Tests that
  only cover the happy path can miss critical bugs in boundary conditions and special
  scenarios.
repository: JetBrains/kotlin
label: Testing
language: Kotlin
comments_count: 7
repository_stars: 50857
---

Ensure tests verify both basic functionality and edge cases. Tests that only cover the happy path can miss critical bugs in boundary conditions and special scenarios.

For each feature:
1. Identify edge cases (empty inputs, null values, boundary values)
2. Test all API functions and variations 
3. Place assertions immediately after the code being tested

Example:

```kotlin
@Sample
fun contains() {
    // Basic functionality
    val string = "Kotlin 1.4.0"
    assertPrints(string.contains("K"), "true")
    assertPrints(string.contains("k"), "false")
    
    // Edge cases
    assertPrints("".contains(""), "true") // Empty receiver and parameter
    assertPrints("Kotlin".contains(""), "true") // Empty parameter
    assertPrints("".contains("Kotlin"), "false") // Empty receiver
    assertPrints("Kotlin".contains("Kotlin"), "true") // Identical strings
    assertPrints("Kotlin 2.0.0".contains("Kotlin"), "true") // Receiver contains parameter
    assertPrints("Kotlin".contains("Kotlin 2.0.0"), "false") // Parameter contains receiver
}
```

Include specific tests for error conditions using explicit assertions rather than try/catch blocks:

```kotlin
// Incorrect: Test passes even if cast doesn't fail
try {
    BNativeHeir as A.Companion
} catch (e: Exception) {
    assertTrue(e is ClassCastException)
}

// Correct: Test only passes if cast fails with expected exception
assertFailsWith<ClassCastException> {
    BNativeHeir as A.Companion
}
```

Comprehensive testing prevents code from "rotting" and ensures reliability across all usage scenarios.
