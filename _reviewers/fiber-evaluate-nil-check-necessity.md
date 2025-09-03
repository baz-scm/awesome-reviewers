---
title: Evaluate nil check necessity
description: Before adding nil checks, evaluate whether they are actually necessary
  or if they represent false positives from static analysis tools. Consider Go's built-in
  nil safety patterns and semantics.
repository: gofiber/fiber
label: Null Handling
language: Go
comments_count: 5
repository_stars: 37560
---

Before adding nil checks, evaluate whether they are actually necessary or if they represent false positives from static analysis tools. Consider Go's built-in nil safety patterns and semantics.

Key principles:
1. **Add explicit nil validation for public API parameters** that could reasonably be nil, especially when the function would panic or behave unexpectedly
2. **Question nil checks flagged by static analysis tools** - tools like nilaway can produce false positives where nil states are impossible given the code flow
3. **Leverage Go's nil-safe operations** - operations like `len(data)` return 0 for nil slices/maps, making explicit nil checks often redundant
4. **Distinguish between nil and zero values** - understand that `[]string{}` (empty slice) and `[]string(nil)` (nil slice) have different semantics, though both have length 0

Example of necessary nil check:
```go
// NewWithClient creates a client from an existing fasthttp.Client
func NewWithClient(c *fasthttp.Client) *Client {
    if c == nil {
        panic("client cannot be nil")
    }
    return &Client{client: c}
}
```

Example of unnecessary nil check:
```go
func parseToStruct(data map[string][]string) error {
    // Unnecessary: len(nil) == 0 in Go
    if data == nil {
        return nil
    }
    // Better: direct length check handles nil case
    if len(data) == 0 {
        return nil
    }
}
```

When in doubt, consider: "Can this value actually be nil given the calling context?" and "Does Go already handle this nil case safely?"