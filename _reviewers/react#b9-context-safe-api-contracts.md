---
title: Context-Safe API Contracts
description: 'Treat API surfaces as contracts: they must be valid for the caller’s
  execution context, use stable/evolvable shapes, and have explicit semantics.


  Standards:'
repository: facebook/react#b9
label: API
language: JavaScript
comments_count: 5
repository_stars: 251891
---

Treat API surfaces as contracts: they must be valid for the caller’s execution context, use stable/evolvable shapes, and have explicit semantics.

Standards:
- Fail fast for invalid context: do not provide silent no-op exports when an API is server-only (or otherwise invalid) in a context. Instead, make importing/using it in the wrong context throw or produce an early, actionable error.
- Prefer options bags for extensibility: for public/tool-facing functions, use a single `options` object (so adding fields doesn’t require signature churn and matches “object-of-arguments” schemas).
- Make required parameters explicit: avoid passing `undefined` as a placeholder when the API can require parameters and let implementations/bindings decide actual values.
- Preserve backwards compatibility for unversioned APIs: if a consumer can’t negotiate versions (e.g., DevTools integration), keep the argument/behavior contract stable.
- Document precise semantics: when parameters are “hints” vs “limits”, or when units differ (code units vs bytes), encode that meaning in docs/types (and align implementation behavior to it).

Example pattern:
```js
// Wrong-context usage should error early.
export function createLedger() {
  if (typeof window !== 'undefined') {
    throw new Error('createLedger() is server-only and cannot be used in client components.');
  }
  // ...server implementation
}

// Tool/public API shape: options bag.
export function getComponentByUid(uid, options) {
  const {includeHooks = false} = options ?? {};
  // ...
}

// Required params: don’t rely on implicit undefined placeholders.
export function preinitModuleForSSR(href, {nonce, integrity, fetchPriority}) {
  // bindings decide how to apply these values
}
```