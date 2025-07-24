---
title: Consistent descriptive naming
description: Ensure variable, function, and type names are consistent, descriptive,
  and follow Go naming conventions. Names should clearly convey their purpose and
  maintain consistency across related components.
repository: prometheus/prometheus
label: Naming Conventions
language: Go
comments_count: 13
repository_stars: 59616
---

Ensure variable, function, and type names are consistent, descriptive, and follow Go naming conventions. Names should clearly convey their purpose and maintain consistency across related components.

Key principles:
- Use descriptive names that accurately reflect functionality rather than generic terms
- Maintain consistent naming patterns across related components (e.g., `EnableTypeAndUnitLabels` vs `AddTypeAndUnitLabels`)
- Follow Go conventions: omit "Get"/"List" prefixes for accessors, use camelCase for JSON fields, proper casing for initialisms
- Avoid misleading names where the name doesn't match the actual behavior

Examples:
```go
// Bad: Generic and inconsistent
func validateAttributes(attrs []string) // actually modifies input
var DefaultRegistry = prometheus.NewRegistry() // in main.go, shouldn't be exported
func handleOtlp(...) // inconsistent casing of initialism

// Good: Descriptive and consistent  
func sanitizeAttributes(attrs []string) // clearly indicates modification
var registry = prometheus.NewRegistry() // unexported, no misleading "Default"
func handleOTLP(...) // consistent initialism casing
func BlockMetas() []BlockMeta // follows Go getter convention
func parseGoDuration(d string) time.Duration // accurately describes return type
```

This approach reduces cognitive load, improves code maintainability, and ensures the codebase follows established Go idioms.