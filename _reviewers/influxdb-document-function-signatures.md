---
title: Document function signatures
description: Always document function parameters and return values in the function
  header comment or interface definition. This is particularly important when a function
  returns multiple values or when the meaning of return values might not be immediately
  obvious.
repository: influxdata/influxdb
label: Documentation
language: Go
comments_count: 2
repository_stars: 30268
---

Always document function parameters and return values in the function header comment or interface definition. This is particularly important when a function returns multiple values or when the meaning of return values might not be immediately obvious.

Example:

```go
// PlanOptimize performs optimization planning and returns three values:
// - []CompactionGroup: groups of files to compact
// - int64: estimated bytes that will be written
// - int64: the generation length
func PlanOptimize() ([]CompactionGroup, int64, int64)
```

By clearly documenting what each return value represents, you make the code more maintainable and reduce the cognitive load for other developers who need to use your functions. Documentation should be placed in the function header comment rather than as a separate comment within the function body.