---
title: Use environment-independent defaults
description: When designing configuration options, avoid relying on environment-specific
  defaults such as system character encodings, file paths, or platform-specific features.
  Instead, specify explicit defaults that work consistently across all supported environments.
  This prevents subtle bugs that manifest only in specific environments.
repository: spring-projects/spring-framework
label: Configurations
language: Java
comments_count: 4
repository_stars: 58382
---

When designing configuration options, avoid relying on environment-specific defaults such as system character encodings, file paths, or platform-specific features. Instead, specify explicit defaults that work consistently across all supported environments. This prevents subtle bugs that manifest only in specific environments.

For example, instead of using default charset for file operations:
```java
// Problematic: relies on environment-specific default charset
new String(Files.readAllBytes(path), Charset.defaultCharset());

// Better: explicitly specifies charset (usually UTF-8)
new String(Files.readAllBytes(path), StandardCharsets.UTF_8);
```

Be especially careful when changing defaults, as this can break existing configurations. Consider IDE compatibility issues when using specific language features or imports, as seen in discussion #3 where a private constant was needed instead of a direct import to avoid Eclipse compilation errors. When updating defaults is necessary, reserve such changes for major version releases to prevent breaking existing tests and deployments.