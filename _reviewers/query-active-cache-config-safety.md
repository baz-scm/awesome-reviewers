---
title: Active Cache & Config Safety
description: 'When implementing caching layers/providers and cache-driven handlers:


  - **Assume multiple cache instances may exist.** Avoid single “default cache” globals
  for runtime behaviors (e.g., focus handlers). Track **all active caches** and update/notify
  each.'
repository: tanstack/query
label: Caching
language: JavaScript
comments_count: 4
repository_stars: 49380
---

When implementing caching layers/providers and cache-driven handlers:

- **Assume multiple cache instances may exist.** Avoid single “default cache” globals for runtime behaviors (e.g., focus handlers). Track **all active caches** and update/notify each.
- **Create cache instances exactly once.** If a cache prop isn’t provided, ensure the provider creates a single cache instance (not a new one per render).
- **Define cleanup semantics for created vs injected caches.** If the provider created a cache, clean it up on unmount and when it’s replaced; if a cache was injected by the parent, do not dispose it inside the provider.
- **Never mutate shared config objects stored in cached entries.** When applying per-query/per-hook config, avoid mutating a config object referenced by another query instance. Prefer replacing with a new merged object.

Example: safe config merge (avoid mutating a shared reference)
```js
// BAD: mutates shared object reference
// Object.assign(query.config, config)

// GOOD: replace with a new merged object
query.config = { ...query.config, ...config }
```

Example: multi-cache handling pattern (conceptual)
```js
// Instead of using a single default cache ref for focus events,
// maintain a registry/list of active caches and notify all.
activeCaches.forEach((cache) => {
  if (/* visible + online */) {
    cache.refetchAllOnWindowFocus?.()
  }
})
```

These rules prevent hard-to-debug cross-query/cross-cache state leaks and make behavior correct under multi-cache usage.