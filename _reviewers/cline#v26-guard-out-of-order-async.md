---
title: Guard Out-of-Order Async
description: 'When async work can overlap (multiple refreshes, navigation, sign-out,
  per-path loads, rapid user actions), never let stale/duplicate completions write
  to shared state. Instead:'
repository: cline/cline#v26
label: Concurrency
language: TSX
comments_count: 5
repository_stars: 70893
---

When async work can overlap (multiple refreshes, navigation, sign-out, per-path loads, rapid user actions), never let stale/duplicate completions write to shared state. Instead:

1) Add a generation/token per operation (or per key)
- Bump the token when starting a new request or when invalidating prior results (e.g., Sign Out, switching context, new refresh).
- After every await (or at least right before any state write), check the token; if it changed, drop the result.
- For map-like caches, use per-key generations so one path’s stale response can’t overwrite another.

2) For “read once / side-effect” async actions, use a single in-flight guard
- If the same operation can be triggered twice quickly (e.g., two clicks, Ctrl+V repeats), ensure only one in-flight request can apply results; others should return early until the first settles.

Example pattern (generation + stale-drop):
```ts
const generationRef = useRef(0);

async function refresh() {
  const gen = ++generationRef.current; // invalidate previous work
  setLoading(true);
  try {
    const result = await fetchSomething();

    // Drop if a newer refresh/invalidation started
    if (generationRef.current !== gen) return;

    // Safe: apply only the latest result
    setData(result);
  } finally {
    if (generationRef.current === gen) setLoading(false);
  }
}
```

Example pattern (in-flight guard for duplicate reads):
```ts
const readInFlightRef = useRef(false);

async function pasteFromClipboardOnce() {
  if (readInFlightRef.current) return;
  readInFlightRef.current = true;
  try {
    const text = await readClipboardText();
    if (text) append(text);
  } finally {
    // Optionally delay release to absorb double triggers
    readInFlightRef.current = false;
  }
}
```

Adopt this as a baseline for any UI/state update that follows an async gap and could overlap with user-driven or effect-driven retriggers.