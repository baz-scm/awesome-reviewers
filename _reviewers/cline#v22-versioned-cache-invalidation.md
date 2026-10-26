---
title: Versioned Cache Invalidation
description: 'When implementing caching for async data, apply two rules:


  1) Cache only what can change

  - Don’t reload invariant configuration during routine refreshes. If the backend/environment/app
  target is stable for the app lifetime, resolve it once (e.g., during startup) and
  reuse it.'
repository: cline/cline#v22
label: Caching
language: TSX
comments_count: 2
repository_stars: 70886
---

When implementing caching for async data, apply two rules:

1) Cache only what can change
- Don’t reload invariant configuration during routine refreshes. If the backend/environment/app target is stable for the app lifetime, resolve it once (e.g., during startup) and reuse it.

2) Prevent stale async responses from overwriting fresh cache
- For cached reads keyed by some identifier (e.g., file path), use a per-key version/generation token.
- Bump the token whenever you invalidate/drop the cache (refresh, tab close, edit, etc.).
- When an async response returns, only apply it if its generation still matches the latest token; otherwise discard it.

Example pattern (per-key generation):

```ts
const generationByKey = new Map<string, number>();
const [cache, setCache] = useState(new Map<string, unknown>());

function bumpGeneration(key: string) {
  const next = (generationByKey.get(key) ?? 0) + 1;
  generationByKey.set(key, next);
  return next;
}

async function loadKey(key: string) {
  const gen = bumpGeneration(key); // invalidates + captures current generation

  try {
    const result = await fetchSomething(key);

    // Discard superseded responses
    if ((generationByKey.get(key) ?? 0) !== gen) return;

    setCache((prev) => {
      const next = new Map(prev);
      next.set(key, result);
      return next;
    });
  } catch {
    // optional: also guard stale errors with the same generation
  }
}
```

This standard directly addresses cache correctness (out-of-order overwrites) and avoids unnecessary reloads for stable values—both common sources of confusing UI/data bugs in caching-heavy code.