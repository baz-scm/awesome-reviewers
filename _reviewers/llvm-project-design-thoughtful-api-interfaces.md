---
title: Design thoughtful API interfaces
description: When designing APIs, prioritize clarity, appropriate abstraction levels,
  and user experience. Avoid magic numbers or unclear parameters by using named constants
  or helper functions. Choose the right balance between generic and specific interfaces
  - use specific types when the use case is well-defined, but design for genericity
  when supporting multiple...
repository: llvm/llvm-project
label: API
language: C++
comments_count: 5
repository_stars: 33702
---

When designing APIs, prioritize clarity, appropriate abstraction levels, and user experience. Avoid magic numbers or unclear parameters by using named constants or helper functions. Choose the right balance between generic and specific interfaces - use specific types when the use case is well-defined, but design for genericity when supporting multiple contexts or languages.

Consider the user experience by minimizing complex parameter construction. Instead of requiring users to manually construct complex objects, provide convenience methods or specializations.

Example from the discussions:
```cpp
// Instead of magic numbers:
Symbolizer->symbolizeData(SymbolizerPath.str(), {Address, 0})

// Use explicit helpers:
static object::SectionedAddress getSectionedAddress(uint64_t Address) {
  return {Address, object::SectionedAddress::UndefSection};
}
Symbolizer->symbolizeData(SymbolizerPath.str(), getSectionedAddress(Address))

// For return types, prefer specific over generic when appropriate:
std::pair<const NamedDecl *, const WarnUnusedResultAttr *>  // specific
// instead of:
std::pair<const NamedDecl *, const Attr *>  // generic

// Provide convenience builders to avoid complex parameter construction:
builder.create<linalg::MatmulTransposeAOp>(...)  // specialized
// instead of requiring users to construct affine maps manually
```

When designing cross-language or cross-context APIs, consider using discriminator fields or configuration parameters rather than embedding language-specific types in generic structures.