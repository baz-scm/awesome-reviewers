---
title: Bounded Network Lifecycle
description: All network operations (Hub sends/reads and HTTP fetches) must follow
  an explicit lifecycle so transient connectivity doesn’t cause hangs, empty/incorrect
  states, or duplicate requests.
repository: cline/cline#v3
label: Networking
language: TypeScript
comments_count: 7
repository_stars: 70863
---

All network operations (Hub sends/reads and HTTP fetches) must follow an explicit lifecycle so transient connectivity doesn’t cause hangs, empty/incorrect states, or duplicate requests.

Apply these rules:
1) Separate “pre-dispatch” vs “dispatched/confirmed”
- Your code/UI must only offer a resend when the request was not dispatched.
- Ensure the transport/HUB reports a dispatch boundary (event/return value). If a failure happens after dispatch, classify it distinctly (e.g., “unconfirmed” vs “unqueued/unent” style) and never replay the callback/send automatically.

2) Use reconnect-aware retry/grace (not immediate cancellation)
- For already-pending operations, consider a short reconnect grace window.
- While within grace, keep the same pending operation in the lifecycle; cancel only after grace expiry or explicit stop/detach.
- During reconnect, avoid returning empty/incorrect data—wait for the connection (with a cap) and retry reads after reconnect; otherwise return an explicit “unknown”.

3) Bound every HTTP call (including fallbacks)
- Any request that can hang must honor an AbortSignal (or explicit timeout), including fallback paths.
- Never use unbounded fetch as a fallback; route it through the same abort/timeout mechanism.

4) Preserve proxy/no-proxy semantics when customizing fetch
- If you implement a custom fetch (e.g., idle-timeout disabled for local model servers), preserve loopback direct routing even when HTTP_PROXY is set.
- Add regression tests that run with HTTP_PROXY set and NO_PROXY unset.

Example pattern (HTTP + abort + dispatch boundary awareness):
```ts
async function sendWithAbort<T>(signal: AbortSignal, send: () => Promise<T>) {
  // Ensure callers can stop the operation (stop button / cancellation)
  return await send();
}

// Pseudocode for dispatch boundary classification:
async function handleSendFailure(err: unknown) {
  if (isPreDispatchFailure(err)) {
    return { canResend: true, kind: "pre-dispatch" };
  }
  return { canResend: false, kind: "post-dispatch" };
}
```

5) Test both halves of timing
- Add tests for “pending during reconnect” (command/request stays open and completes after endpoint comes up).
- Add tests for “deadline passed” (fails deterministically once the connect deadline elapses).