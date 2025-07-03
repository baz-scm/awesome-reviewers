---
title: Use modern test infrastructure
description: Always add new tests to the current recommended test infrastructure rather
  than legacy systems that are being phased out. This reduces technical debt and ensures
  tests remain maintainable as the codebase evolves.
repository: JetBrains/kotlin
label: Testing
language: Other
comments_count: 2
repository_stars: 50857
---

Always add new tests to the current recommended test infrastructure rather than legacy systems that are being phased out. This reduces technical debt and ensures tests remain maintainable as the codebase evolves.

When adding a new test:
1. Check if there's an ongoing migration effort for test infrastructure
2. Target the new recommended infrastructure
3. Follow project-specific guidelines for test generation

Example:
```kotlin
// Instead of adding to legacy build.gradle:
// standaloneTest("new_feature") {
//     source = "runtime/new_feature/test.kt"
// }

// Add a proper test class to the new infrastructure:
// e.g., in native/native.tests/tests/org/jetbrains/kotlin/konan/test/blackbox/NewFeatureTest.kt
class NewFeatureTest : AbstractNativeTest() {
    @Test
    fun testNewFeature() {
        // Test implementation
    }
}
```

For some test types, you may need to run generation tasks after adding new test data files.
