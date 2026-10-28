---
title: Cache key completeness
description: 'A cache is only as correct as the key and invalidation logic around
  it. Before adding or reviewing a cache, check three things:


  1. **The key must encode every input that affects the cached value''s validity.**
  If any factor can change the correct answer, it belongs in the key (or must trigger
  invalidation), otherwise a stale value is served as current. For...'
repository: cline/cline#;sleep 4;
label: Caching
language: TypeScript
comments_count: 8
repository_stars: 70976
---

A cache is only as correct as the key and invalidation logic around it. Before adding or reviewing a cache, check three things:

1. **The key must encode every input that affects the cached value's validity.** If any factor can change the correct answer, it belongs in the key (or must trigger invalidation), otherwise a stale value is served as current. For example, a session-changes refresh key that only tracked tool calls missed new turns with no tool calls; fixed by folding the user-message count into the key (`${status}:${users}:${tools}`). Likewise, a plugin-inspection cache must key on the plugin's registry state and execution mode, not just file fingerprints, so a plugin disabled or re-enabled mid-session forces a fresh read. A pinned-tool-read cache must key on the tool *and* its arguments so an edited pin doesn't serve the old pin's result.

2. **Invalidate explicitly when a dependent state mutation happens**, rather than relying solely on TTL. When a setting like `cloudSessionsEnabled` changes, the dependent history cache must be invalidated before state is posted back to the UI — don't wait for the next natural TTL expiry. Similarly, a remembered "settled" status must be revalidated against the latest source record every time it's read, not trusted forever once observed.

3. **Give caches a bounded lifecycle**: track byte/item budgets against what's actually stored (not an approximate field name — e.g. checking `mediaType` but missing MCP's `mimeType` let oversized entries evade the eviction budget), and provide a dispose/cleanup path for on-disk or long-lived caches so they don't grow unbounded across restarts or runtimes.

When exact real-time consistency isn't achievable (e.g., a third party can mutate shared state out of band), prefer a short TTL with background revalidation ("stale-while-revalidate": return the cached value immediately, kick off a refresh, and let an explicit "Refresh" action force a reload) over either serving indefinitely-stale data or blocking on every read.