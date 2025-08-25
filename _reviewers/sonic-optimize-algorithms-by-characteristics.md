---
title: optimize algorithms by characteristics
description: When implementing algorithms, make optimization decisions based on the
  specific characteristics of your data types and usage patterns rather than using
  generic approaches. Consider factors like type semantics, memory layout, and processing
  requirements to choose the most appropriate algorithmic strategy.
repository: bytedance/sonic
label: Algorithms
language: Go
comments_count: 3
repository_stars: 8532
---

When implementing algorithms, make optimization decisions based on the specific characteristics of your data types and usage patterns rather than using generic approaches. Consider factors like type semantics, memory layout, and processing requirements to choose the most appropriate algorithmic strategy.

For type handling, select operations that preserve type semantics - for example, when processing int vs uint64, use type-specific operations to avoid incorrect processing:

```go
func OP_int() Op {
    switch _INT_SIZE {
    case 32:
        return OP_i32
    case 64:
        return OP_i64
    default:
        panic("unsupported int size")
    }
}
// Add CompatOp to distinguish int from uint64 processing
p.Add(ir.OP_int(), ir.OP_i)
```

For memory management, tailor initialization strategies based on data characteristics - scan vs noscan types may require different clearing approaches:

```go
// Clear memory for noscan types when makeslice semantics require initialization
if et.PtrData == 0 {
    // Clear [oldLen:newLen] to avoid dirty data for skipped types
}
```

For compilation algorithms, optimize based on code complexity - simple operations like pointer dereferencing can be fully inlined rather than using generic recursion:

```go
// Inline simple pointer operations instead of increasing recursion depth
for et.Kind() == reflect.Ptr {
    // Handle pointer-specific interfaces before dereferencing
    if pt.Implements(jsonUnmarshalerType) {
        // Handle directly without recursion
        return
    }
    et = pt.Elem()
}
```

This approach improves both performance and correctness by matching algorithmic choices to the specific requirements and constraints of your data.