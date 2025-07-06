---
title: Explicit security documentation
description: 'Always provide explicit and accurate documentation for security-related
  configurations, including:


  1. Use proper configuration property syntax with validation where possible (e.g.,
  `configprop:spring.security.oauth2.resourceserver.jwt.audiences[]`)'
repository: spring-projects/spring-boot
label: Security
language: Other
comments_count: 4
repository_stars: 77637
---

Always provide explicit and accurate documentation for security-related configurations, including:

1. Use proper configuration property syntax with validation where possible (e.g., `configprop:spring.security.oauth2.resourceserver.jwt.audiences[]`)

2. Clearly document default security behaviors, especially which endpoints or features are exposed/protected by default

3. Include explicit warnings when documenting configurations that relax security for development tools

4. When showing how to disable security features, clearly state the security implications

Example for development tool security configuration:

```java
// SECURITY WARNING: This configuration exposes the H2 console to anyone 
// and disables CSRF protection. Only use in development environments.
@Bean
public WebSecurityCustomizer h2ConsoleSecurityCustomizer() {
    return (web) -> web.ignoring().requestMatchers(PathRequest.toH2Console());
}
```

In documentation, prefer phrasing like "only the `/health` endpoint is exposed over HTTP by default" rather than vague terms like "secret" to clearly communicate security boundaries.