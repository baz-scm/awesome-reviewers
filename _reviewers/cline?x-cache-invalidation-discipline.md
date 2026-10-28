---
title: Cache invalidation discipline
description: Caches must be explicitly invalidated whenever the underlying data they
  represent changes or the context they were scoped to switches (e.g., account/org
  change, model download/delete, new repo snapshot). Never assume a cache stays valid
  across such transitions — clear or refresh it as part of the same action that caused
  the change, rather than relying on...
repository: cline/cline?x
label: Caching
language: TSX
comments_count: 5
repository_stars: 70983
---

Caches must be explicitly invalidated whenever the underlying data they represent changes or the context they were scoped to switches (e.g., account/org change, model download/delete, new repo snapshot). Never assume a cache stays valid across such transitions — clear or refresh it as part of the same action that caused the change, rather than relying on callers to remember.

When invalidation and in-flight reads can race (e.g., a fetch started before invalidation completing after a newer fetch), guard against stale writes landing on top of fresh data by tagging each cache entry/read with a generation or version counter that is bumped on invalidation; discard results whose generation is outdated instead of blindly overwriting state.

Where caches store derived artifacts (e.g., materialized files from content), prefer content-addressable caching (hash of the underlying data) so repeated writes of identical content are deduplicated rather than accumulating duplicates.

Finally, when invalidating to force a refresh, prefer marking entries "stale" and re-fetching in the background while keeping the previous value on screen, rather than clearing the cache outright — this avoids UI flicker/spinners during routine revalidation (e.g., polling).

Example pattern for safe invalidation with race protection:
```ts
const generationRef = useRef(new Map<string, number>());

function invalidate(keys: Iterable<string>) {
  for (const key of keys) {
    generationRef.current.set(key, (generationRef.current.get(key) ?? 0) + 1);
  }
}

async function readWithGeneration(key: string, fetcher: () => Promise<T>) {
  const generation = generationRef.current.get(key) ?? 0;
  const result = await fetcher();
  if ((generationRef.current.get(key) ?? 0) !== generation) return; // stale, discard
  applyResult(key, result);
}
```

Apply this standard whenever introducing or modifying any cache: identify every mutation/context change that should trigger invalidation, decide whether dedup-by-content is appropriate, and protect against race conditions from concurrent reads.