---
title: Consolidate duplicate configurations
description: Maintain a single source of truth for configuration files instead of
  duplicating them across the codebase. Duplicated configurations (like banned-signatures.txt
  files) lead to maintenance challenges, potential inconsistencies, and confusion
  about which version is authoritative.
repository: quarkusio/quarkus
label: Configurations
language: Txt
comments_count: 2
repository_stars: 14667
---

Maintain a single source of truth for configuration files instead of duplicating them across the codebase. Duplicated configurations (like banned-signatures.txt files) lead to maintenance challenges, potential inconsistencies, and confusion about which version is authoritative.

For shared configuration rules like import bans or code quality checks:
- Create a common configuration file (e.g., banned-signatures-common.txt)
- Reference this common file from different modules when needed
- Document the location of the common file

Example:
Instead of having multiple copies:
```
// In module1/banned-signatures.txt
@defaultMessage Don't use Maven classes. They won't be available when using Gradle.
org.apache.maven.**

// In module2/banned-signatures.txt
@defaultMessage Don't use Maven classes. They won't be available when using Gradle.
org.apache.maven.**
```

Consolidate into a common file:
```
// In common/banned-signatures-common.txt
@defaultMessage Don't use Maven classes. They won't be available when using Gradle.
org.apache.maven.**
```

This approach ensures that when configuration rules need to be updated, the change happens in a single place, maintaining consistency across the codebase.