---
title: Descriptive idiomatic identifiers
description: Use descriptive names for variables, types, and interfaces that follow
  Go language idioms. Avoid single-letter variables or cryptic abbreviations that
  reduce code readability.
repository: gin-gonic/gin
label: Naming Conventions
language: Go
comments_count: 4
repository_stars: 83022
---

Use descriptive names for variables, types, and interfaces that follow Go language idioms. Avoid single-letter variables or cryptic abbreviations that reduce code readability.

Key guidelines:
1. Follow Go interface naming conventions by using the "-er" suffix for interfaces that describe behavior (e.g., `Validator` instead of `ValidatorImp`).

2. Don't repeat the package name in type names. When a type is in a package that describes its domain:
```go
// AVOID
package json
type JsonApi interface { ... }

// PREFER
package json
type API interface { ... }
```

3. Choose descriptive variable names, especially avoiding single letters that can be confused with numbers:
```go
// AVOID
for l := len(skippedNodes); l > 0; l-- {
    // ...
}

// PREFER
for length := len(skippedNodes); length > 0; length-- {
    // ...
}
```

4. Avoid cryptic abbreviations like `ldi` or `ri` in favor of complete words like `levelOneRouterIndex` or `recordIndex`.

Clear, descriptive, and idiomatic naming improves code readability and maintenance, making it easier for team members to understand the code's purpose and behavior without additional context.