---
title: consistent error diagnostics
description: When implementing attributes, language features, or compiler diagnostics,
  always provide explicit error diagnostics rather than default warnings for misuse
  scenarios. Error messages should be clear, specific about the violation, and consistent
  with existing diagnostic patterns in the codebase.
repository: llvm/llvm-project
label: Error Handling
language: Other
comments_count: 2
repository_stars: 33702
---

When implementing attributes, language features, or compiler diagnostics, always provide explicit error diagnostics rather than default warnings for misuse scenarios. Error messages should be clear, specific about the violation, and consistent with existing diagnostic patterns in the codebase.

For attributes, explicitly request error diagnostics using `ErrorDiag` in the `SubjectList` to ensure consistent behavior across all attributes. For custom error messages, follow established naming conventions and provide specific guidance about correct usage.

Example of proper error diagnostic implementation:
```cpp
// In Attr.td - Request explicit error diagnostics
def SYCLExternal : InheritableAttr {
  let Spellings = [Clang<"sycl_external">];
  let Subjects = SubjectList<[Function], ErrorDiag>;  // Use ErrorDiag, not default warning
}

// In DiagnosticSemaKinds.td - Provide clear, specific error messages
def err_sycl_external_invalid_linkage : Error<
  "'sycl_external' can only be applied to functions with external linkage">;
```

This approach ensures users receive immediate, clear feedback about incorrect usage rather than potentially overlooked warnings, leading to better code quality and faster debugging cycles.