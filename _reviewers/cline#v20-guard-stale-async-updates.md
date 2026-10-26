---
title: Guard stale async updates
description: 'When UI state can change while async work is in flight (network calls,
  filesystem listings, timers, global key listeners, clipboard reads), enforce three
  concurrency rules:'
repository: cline/cline#v20
label: Concurrency
language: TSX
comments_count: 5
repository_stars: 70886
---

When UI state can change while async work is in flight (network calls, filesystem listings, timers, global key listeners, clipboard reads), enforce three concurrency rules:

1) **Stale-write prevention (generation/invalidation):** Attach a generation/version to each request or logical resource, and check it after every `await` (and before any state write). Bump/invalidate generations when the resource changes (e.g., sign-out, repo/root change, new request supersedes old).

2) **Single-flight deduping (in-flight guard):** If the same async operation can be triggered rapidly by multiple UI events, allow only one in-flight execution using a ref/lock; early-return when locked, and release after completion (or after a short settling window when races are possible).

3) **Visibility/active-state consistency:** On hide/show or “action mode” transitions, cancel/suspend related listeners/holds and reset timers/flags so re-activation re-arms correctly.

Example patterns (self-contained):

```ts
// 1) Generation guard for stale responses
const genRef = useRef(0);
const invalidate = () => { genRef.current++; };

async function load() {
  const myGen = genRef.current;
  const res = await fetchData();
  if (myGen !== genRef.current) return; // drop stale
  setState(res);
}

// Call invalidate() on sign-out / root switch / new request intent.
```

```ts
// 2) In-flight dedupe for async clipboard read
const inFlightRef = useRef(false);

const pasteFromClipboard = useCallback(async () => {
  if (inFlightRef.current) return;
  inFlightRef.current = true;
  try {
    const text = await readClipboardText();
    if (text) setCustomText(text);
  } finally {
    // Optional settling delay to avoid rapid re-triggers duplicating work
    setTimeout(() => { inFlightRef.current = false; }, 100);
  }
}, []);
```

```ts
// 3) Reset timers/flags on hide/show
const flushTimerRef = useRef<number | null>(null);

function cancelFlush() {
  if (flushTimerRef.current != null) {
    clearTimeout(flushTimerRef.current);
    flushTimerRef.current = null; // ensure re-arming works after restore
  }
}

function onVisibilityHidden() {
  cancelFlush();
  // also reset any “listening/processing” flags or suspended states
}
```

Adopt this standard for every async effect that can race with navigation, auth/session changes, polling, or rapidly repeated input—otherwise late/stale promises and duplicate event-triggered reads will overwrite newer UI state or duplicate user-visible output.