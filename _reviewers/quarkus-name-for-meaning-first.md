---
title: Name for meaning first
description: Choose names that prioritize domain meaning and clarity over implementation
  details. This applies to methods, variables, constants, and configuration properties.
  Names should be immediately understandable to developers working in the domain,
  without requiring knowledge of the underlying implementation.
repository: quarkusio/quarkus
label: Naming Conventions
language: Java
comments_count: 5
repository_stars: 14667
---

Choose names that prioritize domain meaning and clarity over implementation details. This applies to methods, variables, constants, and configuration properties. Names should be immediately understandable to developers working in the domain, without requiring knowledge of the underlying implementation.

Key guidelines:
- Use domain terminology over technical implementation details
- Replace magic numbers with meaningfully named constants
- Name boolean flags and masks to reflect their actual meaning
- Follow standard naming conventions when they exist

Example:
```java
// Avoid implementation-focused naming
private static final int ELEVEN = 11;
private boolean isValid = VALID;

// Prefer domain-meaningful naming
private static final int MIN_APPLICATION_NAME_LENGTH = 11;
private boolean isInvalidated = true;

// Follow standard naming when available
public enum COSEAlgorithmIdentifier {  // Following WebAuthn standard
    // enum values...
}
```

This approach improves code maintainability by making the intent clear and reducing the cognitive load for developers reading the code. It also makes the code more resilient to implementation changes, as the names remain valid even if the underlying implementation evolves.