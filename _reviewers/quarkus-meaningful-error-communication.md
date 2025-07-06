---
title: Meaningful error communication
description: 'Error handling should be designed to provide clear, actionable information
  to developers while avoiding redundancy. Follow these practices:


  1. **Don''t duplicate error reporting** - If you''re throwing an exception, don''t
  also log the same error. This creates noise and confusion.'
repository: quarkusio/quarkus
label: Error Handling
language: Java
comments_count: 7
repository_stars: 14667
---

Error handling should be designed to provide clear, actionable information to developers while avoiding redundancy. Follow these practices:

1. **Don't duplicate error reporting** - If you're throwing an exception, don't also log the same error. This creates noise and confusion.

```java
// BAD:
log.errorf("Error unzipping import file %s: %s", fileName, e.getMessage());
throw new IllegalStateException(String.format("Error unzipping import file %s: %s",
  fileName, e.getMessage()), e);

// GOOD:
throw new IllegalStateException(String.format("Error unzipping import file %s: %s",
  fileName, e.getMessage()), e);
```

2. **Provide actionable error messages** - Include information about what went wrong and how to fix it.

```java
// VAGUE:
throw new DeploymentException(String.format("Class %s has no fields.", className));

// BETTER:
throw new DeploymentException(String.format("Class %s has no fields. Parameters containers are only supported if they have at least one annotated field.", className));
```

3. **Handle unsupported operations gracefully** - When a feature might not be supported by all implementations, use try-catch with informative messages:

```java
try {
  options.setUseAlpn(sslOptions.isUseAlpn());
} catch (UnsupportedOperationException e) {
  log.warn("ALPN configuration not supported by implementation: %s. ALPN setting will be ignored."
    .formatted(options.getClass().getName()));
}
```

4. **Use exceptions for misconfigurations** - Log warnings for non-critical issues, but throw exceptions for misconfigurations that would lead to incorrect behavior:

```java
// NOT IDEAL:
if (hasBasic && hasApiKey) {
  LOG.warn("Multiple authentication methods configured. Defaulting to Basic Authentication.");
  return EsAuth.BASIC;
}

// BETTER:
if (hasBasic && hasApiKey) {
  throw new IllegalArgumentException("Multiple authentication methods configured. Please specify only one authentication method.");
}
```

5. **Design interfaces to prevent errors** - Use language features like abstract methods when you expect implementations to provide functionality, rather than runtime exceptions.