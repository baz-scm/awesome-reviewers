---
title: semantic naming accuracy
description: Ensure that method, variable, and class names accurately reflect their
  actual behavior, purpose, or content. Names should semantically match what they
  represent to prevent confusion and bugs.
repository: ClickHouse/ClickHouse
label: Naming Conventions
language: Other
comments_count: 7
repository_stars: 42425
---

Ensure that method, variable, and class names accurately reflect their actual behavior, purpose, or content. Names should semantically match what they represent to prevent confusion and bugs.

Key principles:
- Method names should match their actual behavior: `detachX()` should perform `get + cancel`, not just `cancel`
- Variable names should reflect their content: `patch_block_indices` not `patch_col_indices` when indexing blocks
- Class names should accurately describe their function: `Serialization` not `Compression` when the class handles serialization
- Method names should be descriptive of their purpose: `shouldSearchForPartsOnDisk()` not `lookOnDisk()`
- Use consistent, accurate terminology throughout: `disk` not `drive` when referring to storage disks

Example of problematic vs. corrected naming:
```cpp
// Problematic - method name doesn't match behavior
void detachParallelReadingExtension(); // actually just clears/cancels

// Corrected - name matches actual behavior  
void clearParallelReadingExtension(); // or implement proper detach semantics

// Problematic - variable name doesn't match content
PaddedPODArray<UInt64> patch_col_indices; // actually indexes blocks

// Corrected - name matches content
PaddedPODArray<UInt64> patch_block_indices;
```

This prevents misunderstandings about code behavior and makes the codebase more maintainable by ensuring names serve as accurate documentation of functionality.