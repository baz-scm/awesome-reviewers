---
title: Guard stale async writes
description: When async requests, effects, or user actions can overlap (sign-out,
  switching tabs/orgs, polling, repeated clicks/pastes, show/hide), ensure only the
  latest intent is allowed to commit state.
repository: cline/cline#v25
label: Concurrency
language: TSX
comments_count: 7
repository_stars: 70891
---

When async requests, effects, or user actions can overlap (sign-out, switching tabs/orgs, polling, repeated clicks/pastes, show/hide), ensure only the latest intent is allowed to commit state.

**Standard**
1. **Generation/token guard for async → state commits**
   - Attach a monotonically increasing `generation` (global or per key like per directory path) to each async “load/refresh”.
   - After each `await`, before any state write, verify the generation still matches the latest.
2. **Avoid stale captured state**
   - Don’t persist/commit values computed from variables captured before an `await` if the user may change selection mid-flight.
   - Prefer either:
     - **No write of derived state** (store only user choices, resolve derived fields from current state), or
     - **Commit via ref/updater** that reads the *current* selection at the time the async finishes.
3. **Deduplicate repeated async triggers (in-flight guards)**
   - For clipboard/IO actions where repeated triggers can overlap, use an `inFlight`/ref guard so only one read can append/commit.
4. **Visibility/unmount hygiene**
   - If hiding/unmounting affects timers/async flushing, reset timer refs and related flags in cleanup so when shown again the async pipeline restarts correctly.

**Example (generation guard pattern)**
```ts
const generationRef = useRef(0);

async function load() {
  const gen = ++generationRef.current;
  setLoading(true);

  const result = await apiCall();
  if (gen !== generationRef.current) return; // drop stale response

  setLoading(false);
  setData(result);
}

function invalidate() {
  generationRef.current++; // prevents any in-flight older results from committing
}
```

**Example (in-flight paste guard)**
```ts
const inFlightRef = useRef(false);

async function pasteFromClipboard() {
  if (inFlightRef.current) return;
  inFlightRef.current = true;
  try {
    const text = await readClipboard();
    append(text);
  } finally {
    inFlightRef.current = false;
  }
}
```

Applying this consistently prevents stale async results from overwriting newer user intent, eliminates duplicate commits from overlapping triggers, and keeps UI/timer state consistent across show/hide or lifecycle changes.