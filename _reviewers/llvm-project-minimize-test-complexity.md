---
title: minimize test complexity
description: Tests should be minimal and focused on the specific functionality being
  verified. Remove unnecessary passes, tools, or operations that aren't directly related
  to what's being tested to reduce noise and improve clarity.
repository: llvm/llvm-project
label: Testing
language: Other
comments_count: 3
repository_stars: 33702
---

Tests should be minimal and focused on the specific functionality being verified. Remove unnecessary passes, tools, or operations that aren't directly related to what's being tested to reduce noise and improve clarity.

Key principles:
- Only include components necessary for the test's purpose
- Choose the most appropriate testing tools (e.g., use `llvm-as -disable-output` for verification tests instead of more complex alternatives)
- Simplify test cases to highlight exactly what's being tested
- Reduce the number of test cases when fewer cases can adequately cover the functionality

Example of improvement:
```
// Before: Includes unnecessary canonicalizer pass
// RUN: mlir-opt %s -convert-complex-to-rocdl -canonicalize | FileCheck %s

// After: Focuses only on the conversion being tested  
// RUN: mlir-opt %s -convert-complex-to-rocdl | FileCheck %s
```

This approach makes tests easier to understand, maintain, and debug while ensuring they remain effective at catching regressions.