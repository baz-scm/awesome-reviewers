---
title: Deterministic Error Propagation
description: When handling async work, cancellation, retries, or hydration/prefetch,
  ensure errors are propagated consistently and control flow can’t leave callers stuck.
repository: tanstack/query
label: Error Handling
language: TypeScript
comments_count: 4
repository_stars: 49380
---

When handling async work, cancellation, retries, or hydration/prefetch, ensure errors are propagated consistently and control flow can’t leave callers stuck.

Apply these rules:
1) **Always settle**: any Promise constructed (or thenable returned) must end in either `resolve(...)` or `reject(...)` along every code path—no “neither called” cases.
2) **Stop after error**: in `try/catch`, once you call `onError(...)` (or `reject(...)`), immediately `return` so success handlers don’t run.
3) **Failover, don’t strand**: when an auxiliary path fails (e.g., restore from storage), catch the failure and fall back to the normal execution path (e.g., proceed to `queryFn`), rather than leaving the query stuck in error/loading forever.
4) **Boundary-aware behavior**: when you disable retries/throwing based on ErrorBoundary reset state, still preserve correct error propagation (don’t prevent settlement).

Example (fixing missed `return`):
```ts
try {
  this.setData(data)
} catch (error) {
  onError(error as TError)
  return // critical: don’t run onSuccess after an error
}
```

Example (never leave a hung promise):
```ts
return new Promise((resolve, reject) => {
  observer.subscribe((result) => {
    notifyManager.batchCalls(() => {
      if (result.isError) return reject(result.error)
      // always resolve on success; if you intentionally skip, still resolve
      return resolve(result.data as any)
    })
  })
})
```