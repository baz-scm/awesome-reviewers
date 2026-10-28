---
title: Guard against stale async results
description: When an async operation (network fetch, remote session creation, directory
  read, clipboard read) can be outlived by an invalidating action — sign-out, reset,
  clear, a newer poll, or just a second concurrent trigger — protect every resulting
  state write with a generation/epoch counter or an in-flight guard so a late or duplicate
  completion can never clobber...
repository: cline/cline#$(sleep 4)
label: Concurrency
language: TSX
comments_count: 6
repository_stars: 70978
---

When an async operation (network fetch, remote session creation, directory read, clipboard read) can be outlived by an invalidating action — sign-out, reset, clear, a newer poll, or just a second concurrent trigger — protect every resulting state write with a generation/epoch counter or an in-flight guard so a late or duplicate completion can never clobber fresher state.

Pattern 1 — generation counter: capture the current generation before starting the async call, bump the generation whenever the underlying state is invalidated, and compare the captured value against the live generation immediately before each state write (re-check after every `await`, not just once at the end).

```ts
const generationRef = useRef(0);

function reset() {
  generationRef.current += 1; // invalidates any in-flight work
  setState(initial);
}

async function load() {
  const generation = generationRef.current;
  const result = await fetchSomething();
  if (generation !== generationRef.current) return; // stale, discard
  setState(result);
}
```

Pattern 2 — in-flight guard / shared promise: when the same async action can be triggered multiple times concurrently (rapid clicks, repeated keypress, re-entrant effects, overlapping requests for the same resource), dedupe with a ref/flag checked before starting and cleared only once the operation fully settles, or memoize the pending promise so later callers await the same result instead of starting a new one.

```ts
const inFlightRef = useRef(false);

async function pasteFromClipboard() {
  if (inFlightRef.current) return;
  inFlightRef.current = true;
  try {
    const text = await readClipboard();
    apply(text);
  } finally {
    inFlightRef.current = false;
  }
}
```

Apply this whenever: a response could be superseded by a newer request for the same key (per-key/per-path generation), a long-running creation could be reattached after the user already moved on (clear/reset bumps generation and drops the pending promise), or a cleanup/reap routine must run exactly once across re-renders or reconnects (memoize at module/ref scope). Always write a regression test that lands the stale/duplicate result after the invalidating action and asserts it is dropped.