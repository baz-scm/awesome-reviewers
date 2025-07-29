---
title: avoid password conversions
description: When handling sensitive data like passwords, avoid unnecessary type conversions
  that create additional copies in memory. Pass char[] arrays directly to methods
  that accept them instead of converting to String and back to char[]. This minimizes
  the number of sensitive data copies in memory and reduces the attack surface.
repository: apache/kafka
label: Security
language: Java
comments_count: 1
repository_stars: 30575
---

When handling sensitive data like passwords, avoid unnecessary type conversions that create additional copies in memory. Pass char[] arrays directly to methods that accept them instead of converting to String and back to char[]. This minimizes the number of sensitive data copies in memory and reduces the attack surface.

Example of what to avoid:
```java
// Problematic: creates unnecessary String copy
byte[] passwordBytes = ScramFormatter.normalize(new String(password).toCharArray());
```

Preferred approach:
```java
// Better: pass char[] directly
byte[] passwordBytes = ScramFormatter.normalize(password);
```

This practice is important because String objects are immutable and remain in memory until garbage collected, while char[] arrays can be explicitly cleared after use.