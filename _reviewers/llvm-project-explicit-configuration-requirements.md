---
title: Explicit configuration requirements
description: Always specify explicit configuration parameters rather than relying
  on default settings that may vary across different build environments or target
  platforms. This is particularly critical in test files where assumptions about default
  compiler settings, target triples, or language standards can cause failures in cross-compilation
  scenarios or different...
repository: llvm/llvm-project
label: Configurations
language: C
comments_count: 2
repository_stars: 33702
---

Always specify explicit configuration parameters rather than relying on default settings that may vary across different build environments or target platforms. This is particularly critical in test files where assumptions about default compiler settings, target triples, or language standards can cause failures in cross-compilation scenarios or different build configurations.

When writing tests, explicitly specify:
- Target architecture and OS when cross-compilation is possible
- Language standard requirements when using version-specific features
- Header search paths when system headers are needed

For example, instead of relying on default compiler behavior:
```c
// Problematic - relies on default target triple
// RUN: %clang %s -Dheader="<stdio.h>" -E | tail -1 | FileCheck %s

// Better - explicit configuration
// RUN: %clang_cc1 -x c++ -internal-isystem %S/Inputs/include %s
```

Or when language features require specific standards:
```c
// Explicit standard specification for C11 features
// RUN: %check_clang_tidy -std=c11-or-later -check-suffix=WITH-ANNEX-K %s
```

This approach prevents build failures when default configurations differ from expectations, such as when LLVM_DEFAULT_TARGET_TRIPLE is overridden or when different C standard versions are used.