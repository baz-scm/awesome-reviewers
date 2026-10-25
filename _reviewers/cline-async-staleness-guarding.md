---
title: Async Staleness Guarding
description: 'When async work can overlap (polling, user-triggered refreshes, sign-out,
  rapid UI interactions, or streaming), treat updates as *stale-capable*: only the
  latest (or the correct sequence) is allowed to write state/side-effects.'
repository: ClInE/cLiNe
label: Concurrency
language: TSX
comments_count: 6
repository_stars: 70838
---

When async work can overlap (polling, user-triggered refreshes, sign-out, rapid UI interactions, or streaming), treat updates as *stale-capable*: only the latest (or the correct sequence) is allowed to write state/side-effects.

Apply this standard:
1. **Use per-resource “generation” tokens** for fetch/read flows that can return out of order. Increment the generation before starting a new request; only apply results if the generation still matches.
2. **Use one-at-a-time locks** for side-effectful operations that must not duplicate (e.g., clipboard reads, sequential prompt dispatch). If a request is already in flight, either return early or chain to the previous acceptance event.
3. **Supersede instead of canceling blindly.** If a newer snapshot/listing arrives, deterministically drop older results rather than letting late responses overwrite fresh UI.
4. **Guard state writes on lifecycle/intent changes** (sign-out, hide/unmount/restore, switching from local to cloud) so late responses can’t reintroduce previous state.

Example pattern (generation per key):
```ts
const generationRef = useRef(new Map<string, number>());

async function readLatest(key: string, loader: () => Promise<string>) {
  const nextGen = (generationRef.current.get(key) ?? 0) + 1;
  generationRef.current.set(key, nextGen);

  const result = await loader();
  if ((generationRef.current.get(key) ?? 0) !== nextGen) return; // stale

  // safe: only the latest request updates state
  setValue(key, result);
}
```

Checklist:
- If the code awaits anything and then writes to state, ask: *“Can a newer action happen before this resolves?”* If yes, add generation/in-flight guarding.
- For “sequence required” behavior, serialize with a shared promise/queue (e.g., prompt dispatch waiting for previous acceptance) rather than firing concurrently.