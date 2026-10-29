---
title: Propagate cancellation signals
description: Many concurrency bugs stemmed from abort/cancellation signals not being
  threaded through every async call, or from async operations that could hang forever
  once a caller stopped waiting. When writing any multi-step async flow (provider
  calls, caches, delays, connection setup, streaming reads), treat the `AbortSignal`/cancellation
  token as a first-class...
repository: promptfoo/promptfoo
label: Concurrency
language: TypeScript
comments_count: 10
repository_stars: 26565
---

Many concurrency bugs stemmed from abort/cancellation signals not being threaded through every async call, or from async operations that could hang forever once a caller stopped waiting. When writing any multi-step async flow (provider calls, caches, delays, connection setup, streaming reads), treat the `AbortSignal`/cancellation token as a first-class parameter that must be:

1. **Accepted and forwarded everywhere** — if a function receives an `abortSignal` (or similar), pass it down to every nested async call it makes (SDK `send()`, `cache.get()`, `setTimeout`-based delays, websocket handshakes, etc.). Don't silently drop it just because the current signature doesn't accept a third argument — extend the signature.
2. **Re-checked after every await, not just before it** — an operation can complete or be scheduled after cancellation was requested but before the `await` resolves (e.g., a cache read finishing after abort). Check `signal.aborted` immediately after each `await`, and prefer `Promise.race`-ing the operation against the signal rather than checking it only at the start.
3. **Used to bound the *entire* flow with one deadline** — when a flow has multiple sequential async phases (e.g., connect → configure → run), establish a single deadline/signal at the start and race the whole flow against it, rather than arming the timer only after setup phases complete.
4. **Guaranteed to settle pending promises on cleanup/disconnect/timeout** — never leave a promise that a caller is awaiting (a handshake, a queued request, an iterator start) unsettled when you cancel, close, or time out that path. Explicitly reject it with a cancellation error before tearing down related state, and avoid races where cleanup clears the only reference needed to settle it (e.g., rejecting *before* clearing the pending-reject callback, not after).
5. **Never silently continue past a detected timeout** — if your code already detects that some async precondition failed (e.g., "iterator never started consuming"), don't log a warning and proceed as if it succeeded; reject/fail the operation so callers don't burn their overall time budget waiting on dead work.

Example of racing a setup phase against the overall deadline instead of arming it late:
```ts
async start(): Promise<ConversationResult> {
  const deadline = Date.now() + this.config.timeoutMs;
  const remaining = () => Math.max(0, deadline - Date.now());

  await raceWithTimeout(this.setup(), remaining()); // connect + configureSession
  return raceWithTimeout(this.runConversation(), remaining());
}
```

Applying this consistently prevents orphaned network requests after cancellation, eval runs that outlive their deadlines, and callers hanging indefinitely on a promise nobody will ever resolve.