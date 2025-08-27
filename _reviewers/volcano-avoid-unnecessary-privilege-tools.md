---
title: avoid unnecessary privilege tools
description: Do not install privilege escalation tools like sudo, su, or doas in containers
  unless they are explicitly required for the application's functionality. Most containers
  run as root by default, making sudo redundant and potentially creating security
  vulnerabilities by expanding the attack surface.
repository: volcano-sh/volcano
label: Security
language: Dockerfile
comments_count: 1
repository_stars: 4899
---

Do not install privilege escalation tools like sudo, su, or doas in containers unless they are explicitly required for the application's functionality. Most containers run as root by default, making sudo redundant and potentially creating security vulnerabilities by expanding the attack surface.

Before adding privilege escalation tools, consider:
- Does the container actually need to switch users during runtime?
- Can the required operations be performed during the build phase instead?
- Are there alternative approaches that don't require privilege escalation?

Example of what to avoid:
```dockerfile
# Unnecessary - container already runs as root
RUN apt-get update && \
    apt-get install -y sudo
```

Example of better approach:
```dockerfile
# Perform operations directly as root during build
RUN apt-get update && \
    apt-get install -y required-package
```

This practice reduces the container's attack surface and follows the principle of least privilege by not providing unnecessary tools that could be exploited by attackers.