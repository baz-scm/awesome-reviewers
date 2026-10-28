---
title: Guard async hook staleness
description: 'When a hook kicks off async work (network calls, awaited sends, timers)
  or keeps state outside the component tree (refs, module-level Maps) so it survives
  unmount/remount, protect against stale continuations and identity mismatches:'
repository: cline/cline?ref=main
label: React
language: TypeScript
comments_count: 3
repository_stars: 70980
---

When a hook kicks off async work (network calls, awaited sends, timers) or keeps state outside the component tree (refs, module-level Maps) so it survives unmount/remount, protect against stale continuations and identity mismatches:

1. Bump a generation/version counter (or capture a binding token) whenever the hook rebinds to a new target (new session, new thread, new props). Before applying the result of an awaited call, compare against the current generation and bail out if it no longer matches:
```ts
const generationRef = useRef(0);

async function bindAndFetch(id: string) {
  generationRef.current += 1;
  const generation = generationRef.current;
  const result = await fetchFor(id);
  if (generation !== generationRef.current) return; // stale: ignore
  applyResult(result);
}
```
Do not trust a ref/variable captured before an `await` to still reflect the current instance — re-validate current state (or the generation token) after the await resolves, not just before it started.

2. When persisting state outside React (e.g., a `Map<key, value>` that outlives component mounts so navigation doesn't lose data), key it by the stable, canonical identity of the entity it represents (e.g., the runtime session ID), not by a transient UI-level ID that can alias to the same entity (e.g., two different thread IDs pointing at one session). Verify there is a single, consistent mapping from UI identity to canonical identity, and migrate/merge entries when that mapping changes.

3. Always clean up and detach on unbind/unmount (e.g., `detach` calls, `clearTimeout`) so retired instances can't keep writing into shared state after they're no longer the active one.

Apply this pattern whenever a hook combines async side effects with state that must survive component remounts, to prevent races where a retired instance clobbers newer state or where cache lookups miss due to key mismatches.