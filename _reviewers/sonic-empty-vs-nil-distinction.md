---
title: Empty vs nil distinction
description: Always distinguish between nil and empty values when handling nullable
  types, as they carry different semantic meanings and can affect program behavior.
  Nil represents the absence of a value, while empty represents a zero-length but
  initialized value.
repository: bytedance/sonic
label: Null Handling
language: Go
comments_count: 2
repository_stars: 8532
---

Always distinguish between nil and empty values when handling nullable types, as they carry different semantic meanings and can affect program behavior. Nil represents the absence of a value, while empty represents a zero-length but initialized value.

This distinction is particularly critical in data serialization/deserialization, where maintaining compatibility with standard library behavior is essential. For slices, maps, and other reference types, ensure your code handles both states appropriately.

Example:
```go
// Good: Properly distinguish between nil and empty slice
if slice == nil {
    // Handle nil case - no slice allocated
    return handleNilSlice()
} else if len(slice) == 0 {
    // Handle empty case - slice allocated but no elements
    return handleEmptySlice()
}

// Good: Use appropriate zero values
// For empty slice, use zerobase pointer (not nil) to match standard library
self.Emit("MOVQ", jit.Imm(_Zero_Base), jit.Ptr(_VP, 0))
```

This practice prevents subtle bugs, maintains type information, and ensures consistent behavior across different execution paths.