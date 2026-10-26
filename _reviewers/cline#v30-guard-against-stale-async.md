---
title: Guard Against Stale Async
description: When an async operation can outlive newer user intent (switches, sign-out,
  visibility changes) or be triggered repeatedly, make state updates “commit-time
  safe”.
repository: cline/cline#v30
label: Concurrency
language: TSX
comments_count: 5
repository_stars: 70894
---

When an async operation can outlive newer user intent (switches, sign-out, visibility changes) or be triggered repeatedly, make state updates “commit-time safe”.

Do:
- Add a per-operation token (generation/requestId) and verify it *after every await* (or just before any state write). If the token is stale, return without mutating state.
- Use “latest intent” at commit time: store the latest selection in a ref (or avoid derived writes entirely by persisting only user intent and recomputing derived state from authoritative sources).
- Reset/clear async machinery on teardown or hide/unmount (e.g., timer refs) so the next mount can re-arm correctly.
- Prevent duplicate async side effects by using an in-flight guard (e.g., clipboard reads) when multiple triggers can fire quickly.

Example (generation + commit-time check):
```ts
const genRef = useRef(new Map<string, number>());
const bump = (key: string) => {
  genRef.current.set(key, (genRef.current.get(key) ?? 0) + 1);
  return genRef.current.get(key)!;
};

async function load(key: string) {
  const myGen = bump(key); // or capture current gen
  setLoading(key, true);

  const result = await fetchSomething(key);
  if ((genRef.current.get(key) ?? 0) !== myGen) return; // stale

  setStateForKey(key, result);
  setLoading(key, false);
}

function onUserIntentChange() {
  bump("the-affected-key"); // invalidates in-flight work
}
```

Example (in-flight guard for repeated triggers):
```ts
const inFlightRef = useRef(false);

async function handleAction() {
  if (inFlightRef.current) return;
  inFlightRef.current = true;
  try {
    const data = await readFromClipboard();
    appendOnce(data);
  } finally {
    inFlightRef.current = false;
  }
}
```

This prevents stale responses from overwriting newer state, eliminates duplicate side effects, and avoids stalled UI caused by incomplete cleanup.