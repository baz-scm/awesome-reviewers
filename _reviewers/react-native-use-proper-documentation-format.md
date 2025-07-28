---
title: Use proper documentation format
description: Use the appropriate documentation format for the target programming language.
  In Kotlin files, use KDoc formatting instead of Javadoc formatting for consistency
  and proper tooling support.
repository: facebook/react-native
label: Documentation
language: Kotlin
comments_count: 2
repository_stars: 123178
---

Use the appropriate documentation format for the target programming language. In Kotlin files, use KDoc formatting instead of Javadoc formatting for consistency and proper tooling support.

**Key differences:**
- Use `[ClassName]` instead of `{@link ClassName}` for type references
- Use `[Runnable]` instead of `{@code Runnable}` for code references  
- Avoid dots before method names in references (use `[setApplication]` not `[.setApplication]`)

**Example:**
```kotlin
// ❌ Incorrect (Javadoc style in Kotlin)
/**
 * Throws an {@link AssertionException} if the current thread is not the UI thread.
 * Before calling build, the following must be called:
 * * [.setApplication]
 */

// ✅ Correct (KDoc style in Kotlin)  
/**
 * Throws an [AssertionException] if the current thread is not the UI thread.
 * Before calling build, the following must be called:
 * * [setApplication]
 */
```

This ensures documentation renders correctly in IDEs and documentation generators, and maintains consistency with language conventions.