---
title: Validate security-sensitive inputs
description: Always use appropriate validation mechanisms for security-sensitive inputs
  to prevent vulnerabilities. When implementing validation for headers, origins, user
  inputs, or any security-related data, consult security documentation and use established
  validators rather than creating custom validation logic.
repository: spring-projects/spring-framework
label: Security
language: Java
comments_count: 1
repository_stars: 58382
---

Always use appropriate validation mechanisms for security-sensitive inputs to prevent vulnerabilities. When implementing validation for headers, origins, user inputs, or any security-related data, consult security documentation and use established validators rather than creating custom validation logic.

For example, when validating CORS requests, ensure proper validation of the Origin header:

```java
// Bad - Missing validation
public static boolean isCorsRequest(HttpServletRequest request) {
    String origin = request.getHeader(HttpHeaders.ORIGIN);
    if (origin == null) {
        return false;
    }
    // No validation of origin value before using it
    return true;
}

// Good - Using proper validation
public static IsCorsRequestResult isCorsRequest(HttpServletRequest request) {
    String origin = request.getHeader(HttpHeaders.ORIGIN);
    if (origin == null) {
        return IsCorsRequestResult.IS_NOT_CORS_REQUEST;
    }
    // Using established validation mechanism
    if (!(new UrlValidator().isValid(origin))) {
        return IsCorsRequestResult.INVALID_CORS_REQUEST;
    }
    // Continue with additional validation if needed
    return IsCorsRequestResult.VALID_CORS_REQUEST;
}
```

Using established validators ensures that your security checks benefit from community-vetted logic that properly handles edge cases. Before implementing security validation, research existing issues and security best practices to ensure you're using the most secure approach.