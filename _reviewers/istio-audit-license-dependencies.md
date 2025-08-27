---
title: audit license dependencies
description: Always verify the licensing compatibility of all dependencies, especially
  in security-critical networking code. GPL and other restrictive licenses can create
  legal compliance issues and security vulnerabilities through forced disclosure requirements
  or usage restrictions.
repository: istio/istio
label: Security
language: C
comments_count: 1
repository_stars: 37192
---

Always verify the licensing compatibility of all dependencies, especially in security-critical networking code. GPL and other restrictive licenses can create legal compliance issues and security vulnerabilities through forced disclosure requirements or usage restrictions.

Before integrating external libraries, headers, or frameworks:
1. Identify all direct and transitive dependencies
2. Check each dependency's license against your project's licensing policy
3. Document any licensing conflicts and their security implications
4. Consider dual-licensing or alternative implementations when conflicts arise

Example from BPF networking code:
```c
// Problematic - GPL-only dependencies
#include <linux/bpf.h>        // GPL license
#include <bpf/bpf_helpers.h>  // GPL license

// Solution - Use dual-licensed alternatives or
// implement compatible functionality
char __license[] __section("license") = "Dual BSD/GPL";
```

License restrictions can compromise security by limiting your ability to patch vulnerabilities, distribute security updates, or maintain code independently. Always audit licensing before committing to dependencies in security-sensitive components.