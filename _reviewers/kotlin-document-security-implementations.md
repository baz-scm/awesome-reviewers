---
title: Document security implementations
description: Always document non-obvious security implementations, especially authentication
  mechanisms, with explanatory comments and references to underlying implementation
  details or documentation. Security-related code should be explicit and clear to
  prevent misunderstandings that could lead to vulnerabilities.
repository: JetBrains/kotlin
label: Security
language: Kotlin
comments_count: 1
repository_stars: 50857
---

Always document non-obvious security implementations, especially authentication mechanisms, with explanatory comments and references to underlying implementation details or documentation. Security-related code should be explicit and clear to prevent misunderstandings that could lead to vulnerabilities.

When implementing credential handling or other security features in ways that might not be immediately obvious to other developers, add comments that explain your design decisions and link to relevant documentation or implementation details.

Example:
```kotlin
// Authentication is implemented following the pattern used in org.eclipse.aether.repository.Authentication
// where all credentials are provided to the builder and consumers decide what to use
// See: org.eclipse.aether.transport.wagon.WagonTransporter#getProxy for implementation details
setAuthentication(
    AuthenticationBuilder().apply {
        with(options) {
            addUsername(username?.let(::tryResolveEnvironmentVariable))
            addPassword(password?.let(::tryResolveEnvironmentVariable))
        }
    }
)
```
