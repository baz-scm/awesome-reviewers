---
title: Connection lifecycle invariants
description: 'Networked work must follow explicit lifecycle invariants to prevent
  duplicate sends, lost replies, hangs, and startup/endpoint race bugs.


  Standard

  1) Define a dispatch boundary'
repository: cline/cline#v4
label: Networking
language: TypeScript
comments_count: 6
repository_stars: 70864
---

Networked work must follow explicit lifecycle invariants to prevent duplicate sends, lost replies, hangs, and startup/endpoint race bugs.

Standard
1) Define a dispatch boundary
- Treat a request as “sent/dispatched” only when the Hub/transport explicitly confirms dispatch (or returns an equivalent signal).
- If a failure occurs after the dispatch boundary, do NOT label it “unsent” and do not offer resend/replay that could duplicate already-dispatched work.

2) Gate work until dependencies are ready
- If commands depend on a Hub/transport that is published before it’s ready, hold those commands until startup/settlement completes.
- While the endpoint is “not ready,” keep the command pending until it can actually send.

3) Handle disconnects with reconnect grace (for pending work)
- For already-pending operations, don’t immediately cancel on transient disconnects unless the operation is explicitly non-recoverable.
- Use a reconnect-grace policy: keep pending state during the grace window; cancel only after grace expiry or explicit stop/detach.

4) Enforce connect deadlines and bounded timeouts
- Every network path (including fallback logic) must either respect the provided AbortSignal/deadline or implement its own timeout.
- Avoid any “bare fetch” fallback that can hang indefinitely on packet drops.

5) Proxy + loopback correctness
- When using proxy-aware HTTP agents, preserve direct routing for loopback/local addresses (e.g., localhost/127.0.0.1/::1), even if HTTP_PROXY is set and NO_PROXY is absent.

Illustrative pattern (stateful command send)
```ts
type SendState =
  | { state: 'queued' }
  | { state: 'dispatch-confirmed'; dispatchId: string }
  | { state: 'completed' }
  | { state: 'failed'; reason: 'pre-dispatch' | 'post-dispatch' };

async function sendWithSafeRetry(send: () => Promise<{ dispatchId?: string }>) {
  let st: SendState = { state: 'queued' };

  try {
    const { dispatchId } = await send();
    if (dispatchId) st = { state: 'dispatch-confirmed', dispatchId };
    st = { state: 'completed' };
    return;
  } catch (e) {
    // If we crossed the dispatch boundary, never replay/resend automatically.
    const reason = st.state === 'dispatch-confirmed' ? 'post-dispatch' : 'pre-dispatch';
    st = { state: 'failed', reason };
    throw e;
  }
}
```

How to apply
- Add integration tests that reproduce startup/endpoint-not-ready races, disconnect/reconnect behavior, and proxy/loopback environments.
- Ensure every failure path carries enough information to classify “pre-dispatch vs post-dispatch” and “timed out vs still pending,” and that the UI/logic only retries when it is provably safe.