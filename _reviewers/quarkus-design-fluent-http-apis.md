---
title: Design fluent HTTP APIs
description: When designing HTTP-related APIs, prioritize readability and intuitiveness
  through well-crafted fluent interfaces. API methods should read naturally in code,
  expressing the developer's intent clearly and concisely.
repository: quarkusio/quarkus
label: API
language: Other
comments_count: 2
repository_stars: 14667
---

When designing HTTP-related APIs, prioritize readability and intuitiveness through well-crafted fluent interfaces. API methods should read naturally in code, expressing the developer's intent clearly and concisely.

Key principles:
1. Use intuitive method names that directly express their purpose
2. Provide concise shortcuts for common operations
3. Ensure method chains read like natural sentences
4. Arrange methods in a logical sequence that mirrors user intent

**Example (Improved)**:
```java
// Preferred style - intuitive and readable
httpSecurity
    .get("/public/*").permit()
    .path("/api/*").authenticated()
    .path("/admin/*").roles("admin");
```

**Example (Avoid)**:
```java
// Avoid - less intuitive naming and structure
httpSecurity
    .path("/public/*").methods("GET").authorization().permit()
    .path("/api/*").authenticationMechanism(new CustomAuthMechanism()).authorization().authenticated()
    .path("/admin/*").authorization().roles("admin");
```

When designing security-related APIs, prefer direct method names like `.authenticated()` instead of more verbose alternatives like `.authenticationMechanism()`. For HTTP method operations, provide shortcuts (`get()`, `post()`, `put()`, `delete()`) rather than requiring verbose method specification.

The goal is to create APIs that are not only powerful but also immediately understandable, reducing cognitive load and making the most common use cases the easiest to express.