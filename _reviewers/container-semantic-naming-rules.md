---
title: Semantic Naming Rules
description: 'Adopt a “meaning-first” naming standard: identifiers must communicate
  semantics, representation, and units—so readers can’t guess.


  Apply:

  - Match behavior: rename helpers/methods when behavior changes (avoid names like
  `installDefaultKernel()` if it no longer does “install default”).'
repository: apple/container
label: Naming Conventions
language: Swift
comments_count: 8
repository_stars: 48787
---

Adopt a “meaning-first” naming standard: identifiers must communicate semantics, representation, and units—so readers can’t guess.

Apply:
- Match behavior: rename helpers/methods when behavior changes (avoid names like `installDefaultKernel()` if it no longer does “install default”).
- Name state consistently: use a clear state model (`state` vs `status`) and prefer enums/computed properties over raw string states like `"running"`.
- Avoid misleading action names: if a function can both “register” and “resume,” rename it to reflect both responsibilities (e.g., `addWaiter` → `addOrResume`).
- Encode units/representations: for numeric quantities, include units in the name (`memoryStringAsMiB`, `sizeInBytes`), especially when converting/parsing.
- Make return values self-describing: name tuple elements or return a struct instead of relying on positional tuple members.
- Follow Swift case conventions: types/protocols `UpperCamelCase`; variables/functions `lowerCamelCase`.

Example pattern:
```swift
// Prefer explicit units
func memoryStringAsMiB(_ s: String) throws -> UInt64 { /* ... */ }

// Prefer named tuple fields or struct
let (totalCount, activeCount, totalSize, reclaimableSize): (Int, Int, UInt64, UInt64) = ...
```