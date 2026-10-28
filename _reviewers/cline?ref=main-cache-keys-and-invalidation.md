---
title: Cache keys and invalidation
description: 'Caches repeatedly went stale because they trusted a value''s continued
  validity instead of checking it. Apply two rules to every cache:


  1. **Key on everything that affects the result.** If any input can change the cached
  output, it must be part of the cache key (or the cache must be explicitly invalidated
  when that input changes). Examples of bugs this...'
repository: cline/cline?ref=main
label: Caching
language: TypeScript
comments_count: 8
repository_stars: 70980
---

Caches repeatedly went stale because they trusted a value's continued validity instead of checking it. Apply two rules to every cache:

1. **Key on everything that affects the result.** If any input can change the cached output, it must be part of the cache key (or the cache must be explicitly invalidated when that input changes). Examples of bugs this prevents: a pinned-tool result cached by stale tool/args after the pin was edited; a "current" flag keyed by a refresh token that didn't change when a new turn had no tool calls; a plugin-inspection cache keyed without the plugin's enabled/disabled state and execution mode; a settings toggle (`cloudSessionsEnabled`) that changed what should appear in history without invalidating the history cache.

2. **Never treat a retained connection, in-memory value, or elapsed time alone as proof of freshness.** Revalidate against the authoritative source on a schedule or on read: a kept-alive host connection is not evidence the remote status hasn't changed since the last observation — re-check it against every newer record version, exactly as you would after a restart. For data that's expensive to re-fetch but can legitimately become stale (e.g., account repositories), use an explicit TTL with stale-while-revalidate: serve the cached value immediately, kick off a background refresh once it ages past the TTL, and let an explicit "Refresh" action force a reload.

Additionally:
- Cache expensive results once at the point of creation (e.g., truncate/store a large tool result once at completion), not on every subsequent read or resume — re-deriving on each read risks re-truncating already-shortened data and wastes work.
- Give every persistent or on-disk cache a disposal/cleanup path; a store with no TTL and no cleanup is a leak, not a cache.
- Make sure the key used to populate a cache is the same key callers will actually use at read time (e.g., a per-workspace cache warmed with the process's launch directory instead of the resolved workspace path warms the wrong entry).

```ts
// Bad: key omits an input (plugin state) that changes the result
cachePluginToolDescriptors(cacheKey, entry);

// Good: key includes every input that can change the cached value
const cacheKey = `${pluginPath}:${state}:${updatedAt}:${executionMode}`;
cachePluginToolDescriptors(cacheKey, entry);
```