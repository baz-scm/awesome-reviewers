---
title: Keep API Types Synced
description: 'Any runtime API you expect developers to use must be discoverable and
  accurate in the public contract: update README/API docs and ensure the method is
  declared in the shipped `.d.ts`. Avoid “hiding” APIs behind missing typings or relying
  on long-lived `@ts-expect-error` type suppressions; fix the types/integration so
  the typed contract matches runtime...'
repository: tanstack/query
label: API
language: JavaScript
comments_count: 2
repository_stars: 49380
---

Any runtime API you expect developers to use must be discoverable and accurate in the public contract: update README/API docs and ensure the method is declared in the shipped `.d.ts`. Avoid “hiding” APIs behind missing typings or relying on long-lived `@ts-expect-error` type suppressions; fix the types/integration so the typed contract matches runtime behavior.

Practical checks:
- If a method exists (e.g., `cancel()`), confirm it’s:
  - documented in the public API/README
  - exported/declared in `.d.ts`
  - consistent with the runtime semantics
- If you see a `@ts-expect-error` in a place that affects integration/public config, create a follow-up to remove it once types are corrected.

Example (prefer existing API + ensure it’s part of the public contract):
```js
// Prefer the dedicated API if it exists.
query.clear = () => {
  // Use public, typed method instead of duplicating internals.
  if (query.cancel) query.cancel()
  else {
    clearTimeout(query.staleTimeout)
    clearTimeout(query.cacheTimeout)
  }
}

// Then ensure docs + .d.ts include `cancel(): void` (or the correct signature).
```