---
title: minimize security dependencies
description: 'For security-sensitive operations like shell argument parsing, input
  validation, or cryptographic functions, prefer copying minimal, well-understood
  code over adding external dependencies, especially when:'
repository: kubernetes/kubernetes
label: Security
language: Other
comments_count: 1
repository_stars: 116489
---

For security-sensitive operations like shell argument parsing, input validation, or cryptographic functions, prefer copying minimal, well-understood code over adding external dependencies, especially when:

1. Only a small portion of the dependency's functionality is needed
2. The dependency has limited maintainership (single contributor, few stars/forks)
3. The security implications of the code are significant
4. The copied code is small and easily auditable

This approach reduces attack surface, eliminates supply chain risks, and ensures long-term maintainability of security-critical code paths.

Example: Instead of adding a new dependency for shell argument splitting:
```go
// Prefer: Copy the specific function needed
func splitShellArgs(s string) ([]string, error) {
    // Implementation copied and audited locally
}

// Avoid: Adding dependency with unclear maintenance
import "github.com/unknown-maintainer/shlex"
```

When the functionality is minimal and security-sensitive, the maintenance burden of copied code is often preferable to the risks of external dependencies.