---
title: Descriptive consistent naming
description: Use clear, descriptive names instead of cryptic abbreviations, and follow
  consistent naming patterns across your codebase. This practice enhances readability
  and maintainability.
repository: quarkusio/quarkus
label: Naming Conventions
language: Other
comments_count: 3
repository_stars: 14667
---

Use clear, descriptive names instead of cryptic abbreviations, and follow consistent naming patterns across your codebase. This practice enhances readability and maintainability.

For configuration properties and attributes:
- Prefer full terms over abbreviations (e.g., `authentication-token` instead of `otac`)
- Use lowercase consistently (e.g., `jdk-version-latest` instead of `JDK-ver-latest`)

For package naming:
- Follow established naming conventions (e.g., `io.<organization>.<component-name>`)
- Consider namespace conflicts when defining new package hierarchies
- Use descriptive package names that clearly indicate their purpose

For all identifiers, choose terms that avoid ambiguity with similar concepts in your domain to prevent confusion.

Example:
```properties
# Less clear:
quarkus.http.auth.form.otac.enabled=true

# More clear:
quarkus.http.auth.form.authentication-token.enabled=true
```

```java
// Less clear package structure
package io.quarkus.cache;

// More clear and consistent package structure
package io.quarkus.extension.cache;
```