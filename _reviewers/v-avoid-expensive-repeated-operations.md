---
title: avoid expensive repeated operations
description: Cache results of expensive computations and order operations from cheapest
  to most expensive to minimize performance overhead. This includes storing function
  call results in local variables, extracting constants to avoid repeated allocations,
  using appropriate buffer sizes, and placing fast conditional checks before slower
  ones.
repository: vlang/v
label: Performance Optimization
language: Other
comments_count: 13
repository_stars: 36582
---

Cache results of expensive computations and order operations from cheapest to most expensive to minimize performance overhead. This includes storing function call results in local variables, extracting constants to avoid repeated allocations, using appropriate buffer sizes, and placing fast conditional checks before slower ones.

Key optimization strategies:
- **Cache expensive function calls**: Store results like `node.fkey()`, `expr.expr.str()`, or `c.g.fn_addr.keys()` in local variables when used multiple times
- **Extract constants**: Move unchanging data structures outside functions to avoid repeated allocations per call
- **Order conditions efficiently**: Place cheaper checks (like flag comparisons) before expensive operations (like string comparisons or function calls)
- **Size buffers appropriately**: Use `s.len` instead of arbitrary numbers for initial buffer capacity to minimize reallocations
- **Avoid unnecessary operations**: Use methods like `bytestr()` instead of `str()` when you don't need to empty the buffer

Example of caching expensive operations:
```v
// Before: expensive repeated calls
if !n.contains('.') && n !in c.g.fn_addr.keys() {
    // ... later in code
    if n !in c.g.fn_addr.keys() {
        // keys() called again
    }
}

// After: cache the expensive result
fn_addr_keys := c.g.fn_addr.keys()
if !n.contains('.') && n !in fn_addr_keys {
    // ... later in code  
    if n !in fn_addr_keys {
        // reuse cached result
    }
}
```

Example of condition ordering:
```v
// Before: expensive check first
if node.expr is ast.StringLiteral && node.field_name == 'str' && !f.pref.backend.is_js()

// After: cheap check first
if !f.pref.backend.is_js() && node.field_name == 'str' && node.expr is ast.StringLiteral
```