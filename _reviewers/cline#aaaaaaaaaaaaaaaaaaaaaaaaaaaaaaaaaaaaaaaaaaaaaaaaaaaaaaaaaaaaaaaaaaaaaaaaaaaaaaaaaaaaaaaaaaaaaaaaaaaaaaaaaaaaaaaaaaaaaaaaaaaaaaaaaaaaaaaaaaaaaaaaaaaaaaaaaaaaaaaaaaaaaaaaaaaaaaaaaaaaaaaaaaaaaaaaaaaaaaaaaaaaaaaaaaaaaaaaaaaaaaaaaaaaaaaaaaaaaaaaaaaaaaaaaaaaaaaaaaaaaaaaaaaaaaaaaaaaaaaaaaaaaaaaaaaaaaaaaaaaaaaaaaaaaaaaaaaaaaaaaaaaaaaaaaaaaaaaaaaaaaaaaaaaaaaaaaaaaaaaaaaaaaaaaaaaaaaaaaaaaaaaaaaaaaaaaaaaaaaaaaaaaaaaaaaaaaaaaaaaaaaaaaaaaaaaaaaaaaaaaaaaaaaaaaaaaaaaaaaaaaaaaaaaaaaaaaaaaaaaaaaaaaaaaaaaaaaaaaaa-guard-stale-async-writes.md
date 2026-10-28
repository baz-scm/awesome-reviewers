---
title: Guard stale async writes
description: Async operations (network fetches, clipboard reads, repository/session
  lookups, etc.) can resolve after the state they were meant to update has already
  moved on — the user signed out, reset the view, issued a newer request, or changed
  a selection. Without protection, the stale result lands last and silently overwrites
  fresher state, causing bugs like...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Concurrency
language: TSX
comments_count: 9
repository_stars: 70964
---

Async operations (network fetches, clipboard reads, repository/session lookups, etc.) can resolve after the state they were meant to update has already moved on — the user signed out, reset the view, issued a newer request, or changed a selection. Without protection, the stale result lands last and silently overwrites fresher state, causing bugs like reattaching a cleared chat to an old cloud session, showing a signed-out user's stale account data, or double-appending a pasted clipboard value.

Apply these rules whenever dispatching async work whose result writes to shared/component state:

1. Capture a generation/request token (a ref or counter) immediately before starting the async call, and increment it on any action that invalidates in-flight work (reset, cancel, sign-out, newer request of the same kind, explicit user override).
2. After every `await`, and before performing any state write, re-check that the captured token still matches the current token. If it doesn't, drop the result instead of applying it.
3. For actions that must not run twice concurrently (e.g., a clipboard read, a "create session" call), use an in-flight guard (a promise/boolean ref) so a second trigger reuses or waits on the pending call rather than issuing a duplicate.
4. Where possible, prefer restructuring to remove the race entirely rather than only patching with a token — e.g., make the async path read-only (never write authoritative state) and let a single, synchronous source of truth own writes.

Example pattern:
```ts
const generationRef = useRef(0);

async function reset() {
  generationRef.current++; // invalidate any in-flight work
  setState(initialState);
}

async function load() {
  const generation = ++generationRef.current;
  const result = await fetchSomething();
  if (generation !== generationRef.current) return; // stale, drop it
  setState(result);
}
```

Cover these races with tests that resolve a stale call after a newer one (or after an invalidating action) and assert the stale result is dropped.