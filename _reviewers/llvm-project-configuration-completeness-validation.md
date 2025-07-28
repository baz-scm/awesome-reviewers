---
title: Configuration completeness validation
description: Ensure configuration options are complete and properly validated before
  use. When implementing configuration parsing or option handling, verify that all
  expected cases are covered and add appropriate validation checks for user inputs.
repository: llvm/llvm-project
label: Configurations
language: C++
comments_count: 4
repository_stars: 33702
---

Ensure configuration options are complete and properly validated before use. When implementing configuration parsing or option handling, verify that all expected cases are covered and add appropriate validation checks for user inputs.

Key practices:
1. **Complete option coverage**: When implementing configuration switches or parsers, ensure all documented or expected options are handled. Missing cases can lead to silent failures or unexpected behavior.

2. **Input validation**: Add sanity checks for user-provided configuration values, especially when they override compiler-determined settings.

3. **Required attribute verification**: When configuration depends on specific attributes or flags being present, validate their existence early in the process.

Example from MinGW CRT DLL configuration:
```cpp
// Ensure all expected CRT DLL versions are handled
Opts.MinGWCRTDll = llvm::StringSwitch<enum LangOptions::WindowsCRTDLLVersion>(A->getValue())
    .StartsWithLower("crtdll", LangOptions::WindowsCRTDLLVersion::CRTDLL)
    .StartsWithLower("msvcrt10", LangOptions::WindowsCRTDLLVersion::MSVCRT10)
    // ... other cases ...
    .StartsWithLower("msvcrt-os", LangOptions::WindowsCRTDLLVersion::MSVCRT_OS) // Don't miss expected cases
    .Default(LangOptions::WindowsCRTDLLVersion::Unknown); // Handle unexpected input
```

Example of validation for user input:
```cpp
// Validate user-specified vector sizes
if (!inputVectorSizes.empty()) {
    assert(inputVectorSizes.size() == expectedSize && 
           "Incorrect number of input vector sizes");
    // Add runtime validation for production code
}
```

This prevents configuration-related bugs and ensures robust handling of both expected and edge-case inputs.