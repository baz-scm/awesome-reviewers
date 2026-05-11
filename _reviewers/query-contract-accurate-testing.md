---
title: Contract-Accurate Testing
description: 'Tests should assert the behavior contract precisely, include the missing
  coverage for changed code, and stay isolated/noisy-control friendly.


  Key rules:'
repository: tanstack/query
label: Testing
language: TypeScript
comments_count: 10
repository_stars: 49380
---

Tests should assert the behavior contract precisely, include the missing coverage for changed code, and stay isolated/noisy-control friendly.

Key rules:
- Assert the right semantics: if “no modification” includes referential identity, use `toBe`; if structure matters too, also use `toStrictEqual`.
- Add targeted tests for the actual change (ideally ones that would fail on `main`), including edge paths (e.g., `false` branches).
- For time/async behavior, assert intermediate states at meaningful time points (not only final success).
- When adding type-level guarantees, use Vitest `expectTypeOf` and write assertions that trigger the specific TypeScript checks you care about (e.g., excess properties).
- Keep tests isolated so any test can run independently; mock `console` when tests expect errors to be logged.

Example (identity + deep equality):
```ts
const options = mutationOptions({ mutationKey: ['key'], mutationFn: () => Promise.resolve(5) })
expect(options).toBe(options) // referential identity
expect(options).toStrictEqual({ mutationKey: ['key'], mutationFn: expect.any(Function) })
```

Example (time-based intermediate assertions):
```ts
render(BaseExample, { props: { options: { queries: [/* key1 resolves at 10ms, key2 at 20ms */] } } })
expect(getByText('Status 1: pending')).toBeInTheDocument()
await vi.advanceTimersByTimeAsync(11)
expect(getByText('Status 1: success')).toBeInTheDocument()
await vi.advanceTimersByTimeAsync(10)
expect(getByText('Status 2: success')).toBeInTheDocument()
```

Example (type-test style):
```ts
expectTypeOf(infiniteQueryOptions)
  .parameter(0)
  .not.toHaveProperty('stallTime')
```