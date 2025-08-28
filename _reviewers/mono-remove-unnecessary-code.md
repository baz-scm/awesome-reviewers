---
title: remove unnecessary code
description: Eliminate unnecessary code elements that add complexity without providing
  value. This includes removing redundant function wrappers, unnecessary type annotations,
  singleton classes that could be simple objects, explicit type conversions where
  implicit ones suffice, and methods that duplicate existing functionality.
repository: rocicorp/mono
label: Code Style
language: TypeScript
comments_count: 7
repository_stars: 2091
---

Eliminate unnecessary code elements that add complexity without providing value. This includes removing redundant function wrappers, unnecessary type annotations, singleton classes that could be simple objects, explicit type conversions where implicit ones suffice, and methods that duplicate existing functionality.

Examples of unnecessary code to remove:
- Wrapper functions that don't add logic: `const lock = async () => { ... }; const release = await lock();` → inline the logic directly
- Redundant type annotations: `const BASE_TRANSFORM: any = {...}` → `const BASE_TRANSFORM = {...}`
- Unnecessary type assertions: `satisfies CustomMutatorDefs<typeof schema>` when type inference works
- Explicit conversions: `String(shardNum)` → `shardNum` when concatenating with strings
- Singleton classes: `class ContextManager` with single instance → plain object with functions

Before adding new abstractions, consider if existing functionality can be reused. Before adding type annotations, verify they provide meaningful type safety beyond what TypeScript can infer. This reduces cognitive overhead and makes code more maintainable by focusing on essential logic rather than ceremonial code.