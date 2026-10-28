---
title: Guard stale async results
description: Async operations (network fetches, creates, refreshes, clipboard reads)
  can resolve after the state they were meant to update has already moved on — the
  user signed out, cleared the chat, picked a different item, or triggered a newer
  request. Without protection, the late result overwrites fresher state, causing reattached
  sessions, stale user data,...
repository: cline/cline#|sleep 4
label: Concurrency
language: TSX
comments_count: 8
repository_stars: 70979
---

Async operations (network fetches, creates, refreshes, clipboard reads) can resolve after the state they were meant to update has already moved on — the user signed out, cleared the chat, picked a different item, or triggered a newer request. Without protection, the late result overwrites fresher state, causing reattached sessions, stale user data, flickering UIs, or duplicated side effects.

Apply these two complementary guards wherever concurrent or overlapping async work can occur:

1. **Generation/version tokens for superseded work.** Keep a counter (or similar token) that is bumped whenever an action invalidates in-flight operations (reset, sign-out, new selection, newer request). Capture the current value *before* starting the async call, and re-check it immediately after every `await` and before any state write. If it no longer matches, drop the result silently instead of applying it.

```ts
const generationRef = useRef(0);

function reset() {
  generationRef.current++; // invalidate anything still in flight
  setSessionId(undefined);
}

async function load() {
  const generation = generationRef.current;
  const result = await fetchSomething();
  if (generation !== generationRef.current) return; // superseded, drop it
  setState(result);
}
```

Prefer this per-key (e.g., per path, per repository) when multiple independent async reads can race on different entities, so one entity's staleness doesn't block another's valid update.

2. **In-flight guards for duplicate/overlapping triggers.** When a user action (click, paste, submit) can fire multiple times before the previous async call settles, dedupe or serialize with a ref holding the pending promise. Return/await the existing promise instead of starting a second one, and clear the ref once the operation settles.

```ts
const pendingRef = useRef<Promise<void>>();

async function submit() {
  if (pendingRef.current) return pendingRef.current;
  pendingRef.current = doSubmit().finally(() => {
    pendingRef.current = undefined;
  });
  return pendingRef.current;
}
```

Where possible, prefer removing the race entirely rather than patching around it — e.g., don't let an async lookup write authoritative state directly; instead treat it as a cache that is recomputed from the current source of truth on every read, so a late-arriving response can never clobber a newer user choice.

Add a regression test for every fixed race: hold a slow/old response, trigger the invalidating action, resolve the old response, and assert the stale write never happened.