---
title: Go export naming conventions
description: 'In Go, the first letter of an identifier (function, variable, struct
  field, etc.) determines its visibility outside the package:


  1. **Uppercase first letter**: The identifier is exported and accessible from other
  packages'
repository: kubeflow/kubeflow
label: Naming Conventions
language: Go
comments_count: 7
repository_stars: 15064
---

In Go, the first letter of an identifier (function, variable, struct field, etc.) determines its visibility outside the package:

1. **Uppercase first letter**: The identifier is exported and accessible from other packages
2. **Lowercase first letter**: The identifier is non-exported and only accessible within its package

Always follow these rules:

- Use uppercase for functions intended as public API:
```go
// Exported - can be called from other packages
func DisableCullingAnnotationIsSet(meta metav1.ObjectMeta) bool {
    // implementation
}
```

- Use lowercase for functions meant for internal use only:
```go
// Non-exported - only callable within the same package
func exists(slice []string, val string) bool {
    for _, item := range slice {
        if item == val {
            return true
        }
    }
    return false
}
```

- Name functions to accurately reflect their purpose and return type. Boolean functions should use predicate naming (is*, has*, can*).

- For struct fields, use uppercase to allow external access and lowercase to restrict access:
```go
type MetricsExporter struct {
    Component string    // Exported - accessible
    metricsPort int     // Non-exported - internal only
}
```

- Use consistent error variable names, typically `err` rather than custom names like `kfErr`, `generateErr`, etc.

This convention is a critical part of Go's visibility system and module design - it's not just a style preference but affects how your code can be used by others.
