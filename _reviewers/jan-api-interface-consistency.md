---
title: API interface consistency
description: Ensure that API function signatures, return types, and interface implementations
  are consistent and properly declared. When modifying functions to be asynchronous
  or changing their return types, update both the implementation and any related type
  declarations to maintain contract integrity.
repository: menloresearch/jan
label: API
language: TypeScript
comments_count: 2
repository_stars: 37620
---

Ensure that API function signatures, return types, and interface implementations are consistent and properly declared. When modifying functions to be asynchronous or changing their return types, update both the implementation and any related type declarations to maintain contract integrity.

Key principles:
- Function signatures must match their actual implementation (async functions should be declared as returning Promise)
- Interface implementations should be coherent and focused - prefer implementing multiple feature interfaces rather than extending multiple parent classes
- Runtime type checking considerations should be addressed when designing extensible API interfaces

Example of proper async function declaration:
```typescript
// Good: Declaration matches implementation
async fileStat(path: string, outsideJanDataFolder?: boolean): Promise<FileStat | undefined> {
  // async implementation
}

// Good: Focused interface implementation
export default class JSONConversationalExtension
  implements ThreadExtension, MessageExtension {
  // implements specific feature contracts
}
```

This ensures API consumers can rely on consistent contracts and prevents runtime errors from signature mismatches.