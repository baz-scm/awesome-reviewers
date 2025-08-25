---
title: Function documentation standards
description: Function documentation comments must follow Go conventions by starting
  with the function name, and all parameters should have clear explanations of their
  purpose and current functionality.
repository: bytedance/sonic
label: Documentation
language: Go
comments_count: 2
repository_stars: 8532
---

Function documentation comments must follow Go conventions by starting with the function name, and all parameters should have clear explanations of their purpose and current functionality.

In Go, documentation comments for functions should begin with the function name followed by a description of what it does. Additionally, when functions have parameters that may not be immediately clear, especially those with evolving functionality, include comments that explain their current purpose.

Example of proper function documentation:
```go
// WithCompileRecursiveDepth sets the depth of recursive compile for decoder and encoder.
func WithCompileRecursiveDepth(depth int) CompileOption {
    // implementation
}

// OnObjectBegin handles the beginning of a JSON object value with a
// suggested capacity that can be used to make your custom object container.
// Currently, capacity primarily indicates whether this is an empty node.
func OnObjectBegin(capacity int) error {
    // implementation  
}
```

This ensures that developers can quickly understand function behavior and parameter usage, while also documenting current limitations or evolving functionality for future reference.