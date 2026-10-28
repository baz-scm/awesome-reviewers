---
title: Cache invalidation and freshness
description: 'Caches must stay correct as their underlying inputs change, not just
  fast. When building any cache (in-memory, cross-window, or cross-process), apply
  these rules:'
repository: cline/cline#&&sleep 4
label: Caching
language: TypeScript
comments_count: 6
repository_stars: 70980
---

Caches must stay correct as their underlying inputs change, not just fast. When building any cache (in-memory, cross-window, or cross-process), apply these rules:

1. **Key on everything that affects the result.** A cache key or fingerprint must include every input that can change the correct answer (e.g. a plugin's enabled/disabled registry state and execution mode, not just its file contents). If an input isn't part of the key, a change to that input will silently serve a stale answer.

2. **Invalidate explicitly on every state change that matters.** Don't rely on an unrelated code path to incidentally clear a cache. When a setting or scope that the cache depends on changes (e.g. toggling a feature flag, switching accounts), call the cache's invalidation method directly as part of that change, before the new state is surfaced to consumers.

3. **Use TTL + background refresh for externally-mutable data.** Data that can change outside the app's control (permissions, remote lists, repository access) should never be cached forever nor re-fetched on every read. Serve the cached value immediately, age it out after a reasonable TTL, and refresh it in the background so changes are picked up without UI flicker; still offer an explicit "refresh" path for the user to force a reload.

4. **Never cache a failure as success.** A failed fetch, load, or inspection must not populate the cache, and any "in-flight"/warm-up guard must be released on failure so the next access retries instead of looping forever or permanently serving a degraded result. Only persist clean, successful results.

5. **Centralize cache population.** When multiple entry points can trigger the same warm-up or population logic, consolidate it behind a single hook with a per-key guard (e.g. "warm once per workspace") instead of duplicating warm-up calls at each call site — this avoids redundant work and divergent caching behavior.

Example of invalidating on a relevant state change:
```ts
if (request.cloudSessionsEnabled !== undefined) {
  controller.stateManager.setGlobalState("cloudSessionsEnabled", request.cloudSessionsEnabled)
  // Must invalidate before the new state is posted, or History/UI continues
  // reading the cached enumeration that doesn't yet include/exclude cloud rows.
  controller.invalidateTaskHistoryCache()
}
```