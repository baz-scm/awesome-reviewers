---
title: Consistent terminology usage
description: 'When referring to technical concepts in documentation and code comments,
  use proper full names and consistent terminology:


  1. Use full official names instead of abbreviations or shortened forms (e.g., "Kubernetes"
  instead of "K8s")'
repository: spring-projects/spring-boot
label: Naming Conventions
language: Other
comments_count: 2
repository_stars: 77637
---

When referring to technical concepts in documentation and code comments, use proper full names and consistent terminology:

1. Use full official names instead of abbreviations or shortened forms (e.g., "Kubernetes" instead of "K8s")
2. When describing actions related to annotations, use the verb form without the @ symbol (e.g., use "autowire" as a verb rather than "@Autowire")
3. Follow terminology conventions established in the framework or library documentation

Example:
```
// Incorrect:
// You can @Autowire JdbcTemplate directly into your beans when working with K8s

// Correct:
// You can autowire JdbcTemplate directly into your beans when working with Kubernetes
```

Maintaining consistent terminology improves documentation readability and prevents confusion, especially for developers who are new to the project or technology.