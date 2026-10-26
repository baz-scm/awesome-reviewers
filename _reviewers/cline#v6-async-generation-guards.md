---
title: Async Generation Guards
description: When async work can overlap (polling, retries, out-of-order responses,
  or effect re-runs), you must prevent stale completions from writing state and prevent
  duplicate side effects.
repository: cline/cline#v6
label: Concurrency
language: TSX
comments_count: 7
repository_stars: 70864
---

When async work can overlap (polling, retries, out-of-order responses, or effect re-runs), you must prevent stale completions from writing state and prevent duplicate side effects.

Apply these rules:
1) Use a per-request/per-key generation (or monotonically increasing requestId) and check it right before every state write after an `await`.
2) If you maintain per-item caches (files per path, directories per folder), keep the generation guard per key so a late response can’t overwrite a newer cache entry.
3) For side-effectful async reads (clipboard/paste, mouse+Ctrl+V paths), use an in-flight lock so duplicate triggers can’t append the same data twice.
4) On hide/unmount, clear and reset async schedulers/timers (and any related refs) so re-mounting resumes correctly; for one-time bootstraps, use refs to avoid re-running navigation logic when visibility toggles remount effects.

Example pattern (generation guard):
```ts
const genRef = useRef(0);

const refresh = useCallback(async () => {
  const myGen = ++genRef.current;
  setLoading(true);

  const result = await someAsync();

  // Drop late results
  if (myGen !== genRef.current) return;

  setData(result);
  setLoading(false);
}, []);
```

Example for per-key cache reads:
```ts
const genByKeyRef = useRef(new Map<string, number>());

async function readKey(key: string) {
  const myGen = (genByKeyRef.current.get(key) ?? 0) + 1;
  genByKeyRef.current.set(key, myGen);

  const value = await loadForKey(key);
  if (genByKeyRef.current.get(key) !== myGen) return; // stale

  cache.set(key, value);
}
```

Example for an in-flight side-effect lock (clipboard/paste):
```ts
const inFlightRef = useRef(false);

const pasteFromClipboard = useCallback(async () => {
  if (inFlightRef.current) return;
  inFlightRef.current = true;
  try {
    const text = await readClipboard();
    if (text) append(text);
  } finally {
    // optionally release after a short delay to absorb rapid duplicate triggers
    setTimeout(() => { inFlightRef.current = false; }, 100);
  }
}, [append]);
```

Use this standard for every overlapping async operation that can arrive out of order or be retriggered (pollers, refresh buttons, concurrent loads, visibility transitions, and user-triggered input handlers).