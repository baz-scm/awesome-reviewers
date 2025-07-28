---
title: Avoid unnecessary auto
description: Use explicit types instead of `auto` unless the type is obvious from
  the right-hand side of the assignment or impossible to spell. The LLVM coding standards
  recommend avoiding `auto` in most cases to improve code readability and maintainability.
repository: llvm/llvm-project
label: Code Style
language: C++
comments_count: 10
repository_stars: 33702
---

Use explicit types instead of `auto` unless the type is obvious from the right-hand side of the assignment or impossible to spell. The LLVM coding standards recommend avoiding `auto` in most cases to improve code readability and maintainability.

**When to use `auto`:**
- With explicit casts: `auto *CI = dyn_cast<CallInst>(I)`
- With iterators: `for (auto it = container.begin(); ...)`
- When type is impossible to spell: complex template instantiations
- When type is obvious from context: `auto result = make_unique<MyClass>()`

**When to avoid `auto`:**
- Simple type assignments: Use `StringRef name = getValue()` instead of `auto name = getValue()`
- Function return values: Use `unsigned count = getCount()` instead of `auto count = getCount()`
- Member access: Use `MLIRContext *context = builder.getContext()` instead of `auto context = builder.getContext()`

**Example:**
```cpp
// Bad - type not obvious
auto name = getValue();
auto count = getElementCount();
auto context = builder.getContext();

// Good - explicit types improve readability
StringRef name = getValue();
unsigned count = getElementCount();
MLIRContext *context = builder.getContext();

// Good - auto appropriate here
auto *CI = dyn_cast<CallInst>(instruction);
for (auto it = container.begin(); it != container.end(); ++it) { ... }
```

This practice ensures code remains readable without IDE assistance and makes type information immediately available to reviewers and maintainers.