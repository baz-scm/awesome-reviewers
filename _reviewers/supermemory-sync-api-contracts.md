---
title: Sync API contracts
description: 'Ensure API interfaces are trustworthy and API calls fail safely.


  - Keep typed client contracts aligned with backend reality: if an endpoint exists
  but is missing from the typed client, prefer updating the contract (or generating
  client types) over using `disableValidation`. If you must bypass validation temporarily,
  add a tracked justification.'
repository: supermemoryai/supermemory
label: API
language: TypeScript
comments_count: 2
repository_stars: 28844
---

Ensure API interfaces are trustworthy and API calls fail safely.

- Keep typed client contracts aligned with backend reality: if an endpoint exists but is missing from the typed client, prefer updating the contract (or generating client types) over using `disableValidation`. If you must bypass validation temporarily, add a tracked justification.
- Make failure paths non-destructive: if an API lookup fails, avoid fallback values that can overwrite persisted domain data. Treat failed reads as “no data” so stored fields remain unchanged.
- Respect third-party API limits: implement throttling/rate limiting in the import/caller flow (especially when user actions can trigger many requests) to prevent provider blocks.

Example (safe read + non-destructive failure pattern):
```ts
async function resolveEntityContext(containerTag: string) {
  try {
    const res = await $fetch(`@get/container-tags/${containerTag}`, {
      // ideally, the typed client contract should include this endpoint
      disableValidation: true,
    })
    return res.entityContext ?? undefined
  } catch {
    // important: return undefined so callers do not overwrite stored context
    return undefined
  }
}
```

Example (client-side throttling rationale):
- When importing many items from a provider that blocks bursts, do not fetch everything at once; throttle requests so repeated user actions don’t trigger provider bans.