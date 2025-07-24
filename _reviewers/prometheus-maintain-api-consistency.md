---
title: maintain API consistency
description: When designing or modifying APIs, ensure they follow established patterns
  and conventions within the codebase rather than introducing inconsistent approaches.
  This includes maintaining symmetrical interfaces, preserving backward compatibility
  when possible, and using consistent parameter types across similar functions.
repository: prometheus/prometheus
label: API
language: Go
comments_count: 4
repository_stars: 59616
---

When designing or modifying APIs, ensure they follow established patterns and conventions within the codebase rather than introducing inconsistent approaches. This includes maintaining symmetrical interfaces, preserving backward compatibility when possible, and using consistent parameter types across similar functions.

Key principles:
- Keep existing API signatures intact when adding new functionality, handling differences internally through type assertions or wrapper functions
- Avoid asymmetric designs where related operations (like get/set) use different interface patterns
- Follow established naming and parameter conventions from similar existing functions
- Use consistent interface types across the codebase rather than mixing different approaches

Example from the codebase:
```go
// Instead of exposing non-exported types in public APIs:
func (a *Annotations) Add(err annoErr) Annotations // ❌ Inconsistent

// Keep the established API and handle internally:
func (a *Annotations) Add(err error) Annotations {  // ✅ Consistent
    // Handle type assertions internally
}
```

This approach reduces friction for API consumers, maintains predictable interfaces, and ensures that related functionality follows similar patterns throughout the codebase.