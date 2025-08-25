---
title: Use semantic naming
description: Choose names that clearly communicate the purpose, meaning, and scope
  of variables, functions, constants, and files. Names should be self-documenting
  and immediately convey their role to other developers.
repository: bytedance/sonic
label: Naming Conventions
language: Go
comments_count: 3
repository_stars: 8532
---

Choose names that clearly communicate the purpose, meaning, and scope of variables, functions, constants, and files. Names should be self-documenting and immediately convey their role to other developers.

For constants, use descriptive names that explain what they represent:
```go
// Instead of unclear naming
const APIKind = apiKind

// Use descriptive enum-style naming
type APIKind uint64
const (
    UseSonicJson = iota
    UseStdJson
)
```

For function parameters, ensure names accurately reflect their semantic meaning rather than just their type. For file names, avoid unnecessary specificity when broader scope is appropriate (e.g., `loader_windows.go` instead of `loader_windows_amd64.go` when architecture constraint isn't needed).

The goal is to make code self-documenting through meaningful names that reduce the need for additional comments or context to understand their purpose.