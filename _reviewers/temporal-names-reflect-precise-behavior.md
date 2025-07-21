---
title: Names reflect precise behavior
description: Choose names that accurately reflect the behavior and purpose of code
  elements. Names should be semantically precise and avoid misleading implications.
  This applies to methods, variables, and configuration parameters.
repository: temporalio/temporal
label: Naming Conventions
language: Go
comments_count: 8
repository_stars: 14953
---

Choose names that accurately reflect the behavior and purpose of code elements. Names should be semantically precise and avoid misleading implications. This applies to methods, variables, and configuration parameters.

Key guidelines:
- Method names should accurately describe their behavior (e.g., use 'get' only for methods that return values)
- Avoid generic terms when specific ones better describe the purpose
- Names should reflect what something is or does, not how it's implemented

Examples:
```go
// Misleading - implies just getting indexes
func getIndexes(k string, indexes []int)

// Better - accurately describes behavior of populating the slice
func fillIndexes(k string, indexes []int)

// Misleading - implies attaching something
func attachRateLimiter(config *Config) RateLimiter

// Better - accurately describes creating a new instance
func newDefaultRateLimiter() RateLimiter

// Misleading - implies complete draining
func drainBuffer(items []Item)

// Better - accurately describes partial processing
func processBuffer(items []Item)
```