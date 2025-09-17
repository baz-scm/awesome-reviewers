---
title: avoid suppressing TypeScript errors
description: Do not use `@ts-expect-error` comments to suppress TypeScript errors,
  especially those related to null, undefined, or type safety. These errors are designed
  to catch potential runtime issues and should be properly resolved instead of silenced.
repository: unionlabs/union
label: Null Handling
language: Other
comments_count: 2
repository_stars: 74800
---

Do not use `@ts-expect-error` comments to suppress TypeScript errors, especially those related to null, undefined, or type safety. These errors are designed to catch potential runtime issues and should be properly resolved instead of silenced.

TypeScript's type system helps prevent null reference errors and other type-related bugs. When you encounter type errors, investigate and fix the root cause rather than suppressing them.

Instead of:
```typescript
// @ts-expect-error
someFunction(potentiallyNullValue)
```

Fix the underlying issue:
```typescript
if (potentiallyNullValue !== null) {
  someFunction(potentiallyNullValue)
}
```

Similarly, prefer type-safe patterns like `derived()` stores for read-only computed values instead of `writable()` stores that allow unsafe mutations:

```typescript
// Prefer this - read-only derived state
let destinationChain = derived(chains, $chains => 
  $chains.find(chain => chain.chain_id === destination)
)

// Over this - writable store for derived data
let destinationChain = writable(chains.find(chain => chain.chain_id === destination))
```

If you must temporarily suppress an error during development, add a detailed comment explaining why and create a task to fix it properly.