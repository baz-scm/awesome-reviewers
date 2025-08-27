---
title: Use descriptive, unambiguous names
description: Choose names that clearly communicate their purpose and avoid ambiguity
  or misinterpretation. Names should be self-documenting and consider what developers
  will wonder about at the call site.
repository: bazelbuild/bazel
label: Naming Conventions
language: Java
comments_count: 15
repository_stars: 24489
---

Choose names that clearly communicate their purpose and avoid ambiguity or misinterpretation. Names should be self-documenting and consider what developers will wonder about at the call site.

**Key principles:**
- **Be specific over generic**: Use `isExecutableNonTestRule` instead of `isExecutableRule` when the distinction matters to callers
- **Avoid ambiguous terms**: Replace `underlying` with more precise terms like `hidden` or `server` when the context is unclear
- **Consider call site clarity**: Choose names based on what developers need to understand when using the method
- **Use descriptive constants**: Prefer `UNKNOWN_CPU_TIME` over generic `UNKNOWN` when the context matters
- **Match actual behavior**: Ensure method names like `applyInvalidation` accurately reflect what the method does rather than how it might be interpreted

**Example:**
```java
// Ambiguous - what kind of rule?
public static boolean isExecutableRule(Target target)

// Clear - specifies it excludes test rules  
public static boolean isExecutableNonTestRule(Target target)

// Vague constant
private static final long UNKNOWN = -1;

// Descriptive constant
private static final long UNKNOWN_CPU_TIME = -1;
```

This approach reduces cognitive load, prevents misunderstandings, and makes code more maintainable by ensuring names serve as clear documentation of intent.