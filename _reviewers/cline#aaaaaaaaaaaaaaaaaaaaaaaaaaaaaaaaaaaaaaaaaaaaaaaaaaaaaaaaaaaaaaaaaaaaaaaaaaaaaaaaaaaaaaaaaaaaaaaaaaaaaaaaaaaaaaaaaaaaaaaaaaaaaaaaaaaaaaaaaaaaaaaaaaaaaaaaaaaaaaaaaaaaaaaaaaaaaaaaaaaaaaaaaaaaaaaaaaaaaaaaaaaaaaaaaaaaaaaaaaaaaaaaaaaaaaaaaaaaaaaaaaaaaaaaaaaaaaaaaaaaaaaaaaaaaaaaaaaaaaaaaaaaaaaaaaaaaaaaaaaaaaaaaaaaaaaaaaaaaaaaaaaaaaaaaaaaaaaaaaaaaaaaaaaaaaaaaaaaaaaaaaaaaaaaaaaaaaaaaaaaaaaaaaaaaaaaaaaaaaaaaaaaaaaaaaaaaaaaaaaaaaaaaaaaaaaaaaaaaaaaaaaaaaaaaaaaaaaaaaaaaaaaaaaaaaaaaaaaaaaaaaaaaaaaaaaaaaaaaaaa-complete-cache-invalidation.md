---
title: Complete cache invalidation
description: When caching a computed or fetched value, make the cache key (or refresh
  trigger) include every input that can change the result, and never treat a cached/"remembered"
  value as permanently valid — revalidate it against the authoritative source whenever
  that source could have changed independently of the cache.
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Caching
language: TypeScript
comments_count: 6
repository_stars: 70964
---

When caching a computed or fetched value, make the cache key (or refresh trigger) include every input that can change the result, and never treat a cached/"remembered" value as permanently valid — revalidate it against the authoritative source whenever that source could have changed independently of the cache.

Concretely:
- Audit refresh/invalidation keys for completeness. A key built from only some of the inputs lets unrelated changes slip through as "still current". For example, a UI refresh key based only on tool-call count missed turns with no tool calls; fix by folding in every signal that marks a new unit of work (`${status}:${userMessages}:${toolCalls}`).
- Include state that affects behavior, not just content, in cache keys. A plugin-tools cache keyed only by file contents kept serving stale results after a plugin was disabled/re-enabled; the key must also encode the plugin's registry state (enabled/disabled, last-updated) and execution mode.
- Treat cached "last known status" as a hint, not a fact, once it could be stale. A remembered status from an earlier connection must be re-checked against the record's own version/timestamp (e.g., `updatedAt`) before being trusted again — a retained live handle is not proof the value was continuously observed, so re-validate it the same way you would after a restart.
- Guard against races between cache population and identity/scope changes with a generation counter or epoch check, so a response that resolves after the scope changed (e.g., sign-out during an in-flight sign-in fetch) is discarded rather than cached under the wrong identity.
- For data that can be mutated by other actors (another client, another process, a workspace edit), prefer a short TTL with background revalidation ("stale-while-revalidate") over an unbounded cache, and keep the dependency-tracking layer (e.g., file mtime checks) as the single source of truth rather than adding an extra cache on top that can diverge from it.

Before merging a cache, explicitly list the inputs that determine the cached value and verify the key/invalidation path covers all of them, and write a test that mutates one of those inputs out-of-band and asserts the cache picks up the change.