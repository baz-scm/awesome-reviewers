---
title: Guard stale async results
description: 'When an async operation (fetch, clipboard read, sandbox/session creation,
  directory listing, search) can be triggered again before the previous call resolves,
  protect shared state from being overwritten by a stale, out-of-order completion:'
repository: cline/cline?foo=bar
label: Concurrency
language: TSX
comments_count: 9
repository_stars: 71082
---

When an async operation (fetch, clipboard read, sandbox/session creation, directory listing, search) can be triggered again before the previous call resolves, protect shared state from being overwritten by a stale, out-of-order completion:

1. Tag each request with a generation/epoch counter (or ref) captured before the await; when the call resolves, only apply its result if the counter still matches the latest value. Bump the counter whenever the operation is superseded (new input, reset, clear, cancel).
   ```ts
   const requestId = ++generationRef.current;
   const result = await fetchSomething();
   if (requestId !== generationRef.current) return; // stale, discard
   setState(result);
   ```
2. When operations must not run concurrently (e.g. creating a remote session, dispatching queued prompts), serialize them through a shared promise chain or an in-flight ref so a second call waits for the first to settle instead of racing it, and dedupe identical concurrent triggers (e.g. double paste) with a single in-flight guard that clears after completion.
3. Prefer designs that avoid the race entirely: derive UI state from a single source of truth on every read/render instead of writing to shared state from inside async callbacks. If a cached/read-only check lands late, it should only confirm current state, never overwrite a newer user choice.
4. Don't add staleness guards where there's no async gap to race in — e.g. a synchronous paste event handled inline needs no generation check, only async paths that read external state (clipboard, network) do.

Apply this whenever a component or hook issues network requests, polls, or other re-entrant async work that writes to local/shared state, and explicitly test the "late completion after newer action" scenario (e.g. "keeps selection when a stale lookup resolves after the user already changed it").