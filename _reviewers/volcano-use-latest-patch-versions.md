---
title: Use latest patch versions
description: When configuring dependencies in Dockerfiles and other configuration
  files, use the latest patch versions while keeping major and minor versions fixed.
  Patch versions typically contain important security fixes and bug corrections without
  introducing breaking changes. For example, prefer `golang:1.23.7` over `golang:1.23.0`,
  as "small versions will fix some...
repository: volcano-sh/volcano
label: Configurations
language: Dockerfile
comments_count: 2
repository_stars: 4899
---

When configuring dependencies in Dockerfiles and other configuration files, use the latest patch versions while keeping major and minor versions fixed. Patch versions typically contain important security fixes and bug corrections without introducing breaking changes. For example, prefer `golang:1.23.7` over `golang:1.23.0`, as "small versions will fix some errors." This approach balances stability with security by avoiding breaking changes from major/minor updates while ensuring you receive critical fixes. Apply this consistently across all configuration files in your project.

Example:
```dockerfile
# Good - uses latest patch version
FROM golang:1.23.7 AS builder

# Avoid - missing important patch fixes  
FROM golang:1.23.0 AS builder
```