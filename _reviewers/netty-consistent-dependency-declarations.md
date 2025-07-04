---
title: Consistent dependency declarations
description: Ensure dependency declarations in build configuration files use concrete
  values rather than variables that may not resolve properly at build time. Maintain
  consistency between related configuration files (like BOM and aggregator POMs) to
  prevent build failures.
repository: netty/netty
label: Configurations
language: Xml
comments_count: 3
repository_stars: 34227
---

Ensure dependency declarations in build configuration files use concrete values rather than variables that may not resolve properly at build time. Maintain consistency between related configuration files (like BOM and aggregator POMs) to prevent build failures.

When declaring dependencies in Maven POM files:

1. Avoid using variables in dependency declarations that rely on runtime detection (like `${os.detected.classifier}`)
2. Ensure dependencies are consistently declared across related configuration files
3. Consider using Maven Enforcer's `requireSameVersions` rule for critical dependencies

Example of problematic configuration:
```xml
<dependency>
  <groupId>${project.groupId}</groupId>
  <artifactId>${tcnative.artifactId}</artifactId>
  <classifier>${tcnative.classifier}</classifier>
</dependency>
```

This can result in errors like:
```
Could not find netty-tcnative-2.0.70.Final-${os.detected.classifier}.jar
```

Instead, use concrete values or handle platform-specific dependencies using proper Maven features like profiles or separate platform-specific modules.