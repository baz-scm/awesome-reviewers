---
title: Use defensive null checks
description: When working with properties or methods that could potentially be null,
  use Kotlin's null safety features defensively even if you believe the value should
  never be null. This prevents runtime exceptions when assumptions change or when
  interacting with Java/third-party code.
repository: JetBrains/kotlin
label: Null Handling
language: Kotlin
comments_count: 4
repository_stars: 50857
---

When working with properties or methods that could potentially be null, use Kotlin's null safety features defensively even if you believe the value should never be null. This prevents runtime exceptions when assumptions change or when interacting with Java/third-party code.

Instead of direct access that assumes non-null values:

```kotlin
// Risky: Assumes extensionReceiverParameter, type, and classFqName are all non-null
if (it.owner.extensionReceiverParameter.type.classFqName == receiver) {
    // ...
}
```

Use safe call chains and provide fallback values:

```kotlin
// Safe: Handles potential nulls gracefully
return classOrNull?.let { 
    it.signature?.asPublic()?.let { sig -> 
        sig.packageFqName == packageName && sig.declarationFqName.matches(typeNameReg)
    }
} ?: false

// Another example with safe call chains
if (it.owner.extensionReceiverParameter?.type?.classFqName == receiver) {
    // ...
}
```

This approach is especially important when:
- Working with data from external sources
- Handling return values from Java methods (which might return null despite non-null annotations)
- Dealing with complex object hierarchies
- Creating code that others will depend on

Remember that source locations, error reporting systems, and other infrastructure often assume non-null values. Adding defensive checks prevents crashes even when the underlying problem may be elsewhere.
