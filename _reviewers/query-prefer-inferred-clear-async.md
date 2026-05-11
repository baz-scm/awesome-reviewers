---
title: Prefer inferred, clear async
description: 'When writing code and tests, optimize for clarity and idiomatic TypeScript:


  1) Prefer `async/await` when the async function includes a side effect.

  ```ts'
repository: tanstack/query
label: Code Style
language: TSX
comments_count: 4
repository_stars: 49380
---

When writing code and tests, optimize for clarity and idiomatic TypeScript:

1) Prefer `async/await` when the async function includes a side effect.
```ts
// Clear: side effect is explicit
queryFn: async () => {
  await sleep(10)
  fetched = true
  return 'fetched'
}

// Less explicit when side effects are involved
queryFn: () => sleep(10).then(() => {
  fetched = true
  return 'fetched'
})
```

2) Let TypeScript infer callback types; avoid explicit parameter annotations/imports when they’re redundant.
```ts
// Prefer inference
onMutate: async (newTodo, context) => {
  // ...
}
// If the types infer correctly, remove extra imports/annotations.
```

3) Simplify type-level assertions by removing unnecessary generics/wrappers; use direct indexed access or the minimal expression that captures the intended type.
```ts
// Prefer minimal type plumbing
expectTypeOf(queryKey[dataTagSymbol]).toEqualTypeOf<InfiniteData<string>>()
```