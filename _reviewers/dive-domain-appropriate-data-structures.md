---
title: Domain-appropriate data structures
description: Design data structures that accurately reflect the constraints and behavior
  of your problem domain. Choose data types that match the natural constraints of
  your values, and design structural patterns that align with expected usage.
repository: wagoodman/dive
label: Algorithms
language: Go
comments_count: 2
repository_stars: 51517
---

Design data structures that accurately reflect the constraints and behavior of your problem domain. Choose data types that match the natural constraints of your values, and design structural patterns that align with expected usage.

For numeric fields, use unsigned types when values cannot be negative:
```go
type FileTree struct {
    Root *FileNode
    Size int
    FileSize uint64  // Use uint64 since file sizes cannot be negative
}
```

For tree structures, consider whether structural nodes (like root nodes) should participate in traversal or serve purely as organizational anchors. Document these design decisions to prevent confusion:
```go
// never process the root node - it serves as a structural anchor
// keeping a single root node simplifies traversal compared to multiple roots
if currentNode == tree.Root {
    continue // skip processing, but traverse children
}
```

This approach prevents bugs by encoding domain knowledge directly into the data structure design, making invalid states harder to represent and reducing the need for runtime validation.