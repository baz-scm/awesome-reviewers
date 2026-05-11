---
title: Test error propagation
description: 'When changing error handling, add/maintain tests that:

  - Cover all supported configuration shapes (e.g., `useErrorBoundary: true` and `useErrorBoundary:
  (err) => boolean`).'
repository: tanstack/query
label: Error Handling
language: TSX
comments_count: 5
repository_stars: 49380
---

When changing error handling, add/maintain tests that:
- Cover all supported configuration shapes (e.g., `useErrorBoundary: true` and `useErrorBoundary: (err) => boolean`).
- Assert the exact outcome of error handling logic (e.g., whether an error is redacted during dehydration/rehydration).
- Keep tests deterministic: don’t manipulate `NODE_ENV` or other globals unless the behavior truly differs.
- Ensure the test name/expectations match the real trigger (e.g., the hook that throws and causes the boundary to render).
- Use the correct async error pattern so the error is observed by the code path under test (prefer `Promise.reject(err)` / `then(() => Promise.reject(err))`).

Example (boundary + config variant):

```ts
it('lets errors fall through when useErrorBoundary is falsey', async () => {
  const key = queryKey()

  function Page() {
    useQueries({
      queries: [{
        queryKey: key,
        queryFn: () => Promise.reject(new Error('boom')),
        useErrorBoundary: (err) => err.message.includes('boom'),
      }],
    })

    return null
  }

  // assert: boundary behavior matches the function result
})
```

Example (redaction rule):

```ts
const queryClient = createQueryClient({
  defaultOptions: {
    dehydrate: {
      shouldDehydrateQuery: () => true,
      shouldRedactErrors: () => false,
    },
  },
})

await expect(
  dehydrate(queryClient).queries[0]!.promise,
).resolves.toBeInstanceOf(Promise) // and then assert the thrown error is the original
```

The goal is confidence that error propagation/redaction behaves exactly as intended across supported modes, without relying on brittle or misleading test setup.