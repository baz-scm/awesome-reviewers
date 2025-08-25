---
title: Numeric API completeness
description: When designing APIs that handle numeric values, ensure comprehensive
  support for different integer types (Int64, Uint64) based on range requirements
  and use case needs. Consider practical constraints such as migration costs and legacy
  system compatibility when deciding between unified or separate configuration options.
repository: bytedance/sonic
label: API
language: Go
comments_count: 2
repository_stars: 8532
---

When designing APIs that handle numeric values, ensure comprehensive support for different integer types (Int64, Uint64) based on range requirements and use case needs. Consider practical constraints such as migration costs and legacy system compatibility when deciding between unified or separate configuration options.

For configuration APIs, provide separate options when legacy compatibility is crucial:
```go
type Config struct {
    // Uint64 into strings on Marshal
    Uint64ToString bool
    // Int64 into strings on Marshal (separate option for migration compatibility)
    Int64ToString bool
}
```

For data access APIs, provide complete numeric type coverage:
```go
// Int64 casts the node to int64 value
func (self *Node) Int64() (int64, error) { ... }
// Uint64 casts the node to uint64 value (needed for full range support)
func (self *Node) Uint64() (uint64, error) { ... }
```

This approach ensures APIs can handle the full spectrum of numeric requirements while accommodating real-world migration and compatibility constraints.