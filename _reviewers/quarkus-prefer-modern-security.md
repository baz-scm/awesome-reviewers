---
title: Prefer modern security
description: When implementing security features (such as artifact signing), use current
  best practices and prefer pure-Java security libraries over native executables whenever
  possible. This approach simplifies configuration, improves portability, and reduces
  security risks associated with native executable dependencies and their complex
  configurations.
repository: quarkusio/quarkus
label: Security
language: Xml
comments_count: 1
repository_stars: 14667
---

When implementing security features (such as artifact signing), use current best practices and prefer pure-Java security libraries over native executables whenever possible. This approach simplifies configuration, improves portability, and reduces security risks associated with native executable dependencies and their complex configurations.

For example, when configuring Maven GPG plugin, prefer:
```xml
<configuration>
    <bestPractices>true</bestPractices>
    <useAgent>false</useAgent>
    <signer>bc</signer>
</configuration>
```

Instead of manual configurations with native executables:
```xml
<configuration>
    <!-- Prevent gpg from using pinentry programs -->
    <gpgArguments>
        <arg>--pinentry-mode</arg>
        <arg>loopback</arg>
    </gpgArguments>
</configuration>
```

This leverages libraries like BouncyCastle (Java-based cryptography) that eliminate the need for native GPG executable installation and complex signature setup.