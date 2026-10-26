---
title: Guard Stale Async Writes
description: When async work can overlap (polling, refresh, user-triggered actions,
  or fetches), ensure only the latest/eligible result is allowed to write state or
  cause side effects.
repository: cline/cline#x
label: Concurrency
language: TSX
comments_count: 5
repository_stars: 70861
---

When async work can overlap (polling, refresh, user-triggered actions, or fetches), ensure only the latest/eligible result is allowed to write state or cause side effects.

Apply this standard:
1) Gate state writes with a monotonic token (generation/supersession)
- Create a per-resource generation counter (often per key/path/request).
- Increment it when starting a new operation or when invalidating (e.g., Sign Out, refresh).
- After every await, check the token before mutating state. If it doesn’t match, drop the response.

2) Prevent duplicate side effects with single-flight in-flight guards
- For operations where repeated user actions must not re-apply the same external input (clipboard, double-click, rapid hotkeys), use an in-flight ref/lock.
- Return early while the lock is held; release it after a short settle time or on completion.

3) Prefer designs that remove stale-write pathways
- If an async lookup would otherwise “flip” the current user intent based on an old result, store only user intent and derive the async-dependent values from current state (so late lookups can’t overwrite intent).

4) (Corollary) When UI hide/show unmounts/re-mounts, ensure concurrency-related refs/timers are reset
- Cleanup must clear timers and reset flags/refs that control future async scheduling.

Example (generation gate + drop stale response):
```ts
const generationRef = useRef(new Map<string, number>());
function bump(keys: Iterable<string>) {
  for (const k of keys) {
    generationRef.current.set(k, (generationRef.current.get(k) ?? 0) + 1);
  }
}

async function load(path: string) {
  bump([path]);
  const myGen = generationRef.current.get(path)!;

  const result = await fetchSomething(path);
  if ((generationRef.current.get(path) ?? 0) !== myGen) return; // stale

  setStateForPath(path, result);
}
```

Example (single-flight clipboard/paste):
```ts
const inFlightRef = useRef(false);
const releaseTimerRef = useRef<number | null>(null);

async function pasteFromClipboard() {
  if (inFlightRef.current) return;
  inFlightRef.current = true;

  try {
    const text = await readClipboardText();
    if (text) append(text);
  } finally {
    if (releaseTimerRef.current) window.clearTimeout(releaseTimerRef.current);
    releaseTimerRef.current = window.setTimeout(() => {
      inFlightRef.current = false;
    }, 100);
  }
}
```

Make these checks a default review checklist item for any async callback that updates state, derived selection, or triggers user-visible side effects.