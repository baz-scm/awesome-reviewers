---
title: Use descriptive identifier names
description: Choose specific, descriptive names for variables, functions, types, and
  parameters that clearly indicate their purpose and avoid generic terms that could
  be overloaded or ambiguous. Generic names like `Command`, `Config`, or `Data` can
  become confusing when multiple similar concepts exist in the same codebase.
repository: snyk/cli
label: Naming Conventions
language: Go
comments_count: 2
repository_stars: 5178
---

Choose specific, descriptive names for variables, functions, types, and parameters that clearly indicate their purpose and avoid generic terms that could be overloaded or ambiguous. Generic names like `Command`, `Config`, or `Data` can become confusing when multiple similar concepts exist in the same codebase.

When naming identifiers, consider:
- What specific role or responsibility does this identifier serve?
- Could this name be confused with other similar concepts in the codebase?
- Does the name clearly communicate what the identifier contains or does?

Example of improvement:
```go
// Instead of generic name that conflicts with other Command types
type Command struct {
    // ...
}

// Use specific, descriptive name
type NodeCLICommandMeta struct {
    // ...
}

// Instead of ambiguous function name
func GetGlobalConfiguration() []ConfigOption {
    // ...
}

// Use name that clearly indicates what is returned
func GetGlobalConfigurationOptions() []ConfigOption {
    // ...
}
```

This practice prevents naming conflicts, reduces cognitive load when reading code, and makes the codebase more maintainable as it grows.