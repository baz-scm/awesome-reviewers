---
title: Explicit security configurations
description: 'When configuring security-related features, always use the most specific
  configurer classes to make security decisions explicit and improve code readability.
  For example, when disabling CSRF protection in Spring Security, use `CsrfConfigurer::disable`
  instead of the more generic `AbstractHttpConfigurer::disable`:'
repository: spring-projects/spring-boot
label: Security
language: Java
comments_count: 8
repository_stars: 77637
---

When configuring security-related features, always use the most specific configurer classes to make security decisions explicit and improve code readability. For example, when disabling CSRF protection in Spring Security, use `CsrfConfigurer::disable` instead of the more generic `AbstractHttpConfigurer::disable`:

```java
// Prefer this (explicit about what security feature is being disabled)
http.csrf(CsrfConfigurer::disable);

// Instead of this (less explicit)
http.csrf((csrf) -> csrf.disable());
// or
http.csrf(AbstractHttpConfigurer::disable);
```

This practice improves code clarity, makes security decisions more visible during code reviews, and helps prevent misunderstandings about which security features are being modified. By using type-specific configurers, the code self-documents which security features are being configured, making it easier to audit and maintain security settings over time.