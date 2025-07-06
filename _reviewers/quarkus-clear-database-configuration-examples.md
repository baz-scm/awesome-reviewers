---
title: Clear database configuration examples
description: Database configuration examples in documentation should be correct, minimal,
  and include proper context. Provide only essential configuration properties rather
  than defaults or environment-specific values that would change in production. Use
  proper syntax and be precise about component interactions.
repository: quarkusio/quarkus
label: Database
language: Other
comments_count: 5
repository_stars: 14667
---

Database configuration examples in documentation should be correct, minimal, and include proper context. Provide only essential configuration properties rather than defaults or environment-specific values that would change in production. Use proper syntax and be precise about component interactions.

For configuration properties, always use the correct syntax:
```properties
# Good: Using proper equals sign syntax
quarkus.datasource."named-datasource".reactive = true
quarkus.datasource."named-datasource".db-kind = postgresql

# Bad: Using incorrect comma syntax
quarkus.datasource."named-datasource".reactive", true
quarkus.datasource."named-datasource".db-kind", postgresql
```

When documenting multiple database access approaches (like Hibernate ORM and Hibernate Reactive), clearly explain their boundaries:

```properties
# Note: When using both ORM and Reactive, they won't share the same persistence context
# It's recommended to use ORM in blocking endpoints, and Reactive in reactive endpoints
```

For complex configurations like transaction recovery, include explanatory notes about the consequences of configuration choices:

```properties
# Only disable recovery if you understand the implications
# May result in data loss if disabled incorrectly
quarkus.datasource.jdbc.enable-recovery = false
```

Organize related examples in dedicated sections rather than mentioning capabilities in passing or pointing to test code, which can confuse users.