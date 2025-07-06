---
title: Update vulnerable dependencies
description: Always update dependencies with known security vulnerabilities to their
  patched versions. Dependencies with security issues can introduce vulnerabilities
  into your application even if your own code is secure.
repository: grafana/grafana
label: Security
language: Other
comments_count: 1
repository_stars: 68825
---

Always update dependencies with known security vulnerabilities to their patched versions. Dependencies with security issues can introduce vulnerabilities into your application even if your own code is secure.

When you discover a dependency with a security vulnerability:
1. Check the fixed version information (e.g., "Fixed Version: 0.38.0")
2. Update the dependency in your go.mod file immediately
3. Run tests to ensure compatibility with the updated version

Consider implementing automated dependency scanning in your CI/CD pipeline to proactively identify vulnerabilities before they reach production.

Example:
```go
// Before: Vulnerable dependency
require (
    golang.org/x/net v0.36.0 // Has CVE-2025-22872 vulnerability
)

// After: Updated to patched version
require (
    golang.org/x/net v0.38.0 // Fixes CVE-2025-22872
)
```