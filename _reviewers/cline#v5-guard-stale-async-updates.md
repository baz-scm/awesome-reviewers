---
title: Guard stale async updates
description: 'For any async operation that can overlap (polls, refreshes, snapshot-driven
  reads, delayed directory listings, fetches after user actions, clipboard reads),
  treat state updates as *conditional commits*: only apply results if they still correspond
  to the latest request/action. Otherwise, drop the response or prevent duplicate
  side-effects.'
repository: cline/cline#v5
label: Concurrency
language: TSX
comments_count: 6
repository_stars: 70864
---

For any async operation that can overlap (polls, refreshes, snapshot-driven reads, delayed directory listings, fetches after user actions, clipboard reads), treat state updates as *conditional commits*: only apply results if they still correspond to the latest request/action. Otherwise, drop the response or prevent duplicate side-effects.

Apply these rules:
- **Use generation/requestId tokens** per operation (and per key/path/tab when relevant). Increment before starting; capture token in the async closure; **check token equality before any state write**.
- **Key by resource** (file path, directory path, model name, conversation id). Keep a `Map<key, generation>` so independent reads don’t block each other.
- **Prevent duplicate side-effects** with an **in-flight guard/ref** when the same action can be triggered rapidly (double click / repeated paste): return early while pending, and release when the pending work finishes (optionally with a short settling delay).
- **Prefer “store user intent, not derived async writes”** when possible: store the choice, and recompute derived fields from current state instead of updating user-facing target fields from late lookups.

Example (generation guard per key):
```ts
const genRef = useRef(new Map<string, number>());

function bump(keys: Iterable<string>) {
  for (const k of keys) {
    genRef.current.set(k, (genRef.current.get(k) ?? 0) + 1);
  }
}

async function readResource(key: string) {
  const gen = (genRef.current.get(key) ?? 0) + 1;
  genRef.current.set(key, gen);

  const result = await api.read(key);

  // Commit only if still current.
  if (genRef.current.get(key) !== gen) return;
  setState(prev => ({ ...prev, [key]: result }));
}
```

Checklist for code review:
- Is there any `await`/callback that leads to `setState`/writes, where a newer request could start before the old one resolves?
- If yes, can a late response overwrite newer UI/state? If so, add generation/token checks or switch to an intent-first model.
- If the user can trigger the action repeatedly, is there an in-flight guard to prevent duplicate commits?