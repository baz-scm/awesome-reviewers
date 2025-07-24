---
title: Follow existing naming patterns
description: Maintain consistency with established naming conventions throughout the
  codebase. When adding new flags, functions, or variables, examine existing similar
  implementations and follow the same patterns for naming, separators, and structure.
repository: docker/compose
label: Naming Conventions
language: Go
comments_count: 12
repository_stars: 35858
---

Maintain consistency with established naming conventions throughout the codebase. When adding new flags, functions, or variables, examine existing similar implementations and follow the same patterns for naming, separators, and structure.

Key areas to check:
- **Flag names**: Use consistent naming with existing commands (e.g., `--timestamps` not `--timestamp` to match `compose logs`)
- **Function names**: Choose names that accurately describe behavior (e.g., `GetImageNameOrDefault` instead of `GetDefaultImageName` when reading existing values first)
- **Separators**: Use consistent separators throughout (e.g., `-` for resource names, `:` for label formatting)
- **Parameter names**: Match parameter names to their types and usage (e.g., `streams` not `dockerCli` when type is `api.Streams`)

Example from codebase:
```go
// Consistent with existing logs command
flags.BoolVar(&up.timestamps, "timestamps", false, "Show timestamps.")

// Descriptive function name that matches behavior  
func GetImageNameOrDefault(service types.ServiceConfig, projectName string) string {
    if service.Image != "" {
        return service.Image
    }
    return projectName + "-" + service.Name  // Use consistent separator
}
```

Before introducing new naming, search the codebase for similar functionality and adopt the established patterns to maintain consistency and reduce cognitive load for developers.