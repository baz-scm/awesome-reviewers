---
title: Network boundaries and timeouts
description: 'Ensure networked operations are safe and correct across retries, disconnects,
  and long-running requests.


  Apply this standard:

  1) Always use a hard bound: attach an AbortSignal (and/or explicit timeout) to every
  network call that could otherwise hang. Don’t rely on implicit/idle behavior.'
repository: cline/cline#v8
label: Networking
language: TypeScript
comments_count: 6
repository_stars: 70867
---

Ensure networked operations are safe and correct across retries, disconnects, and long-running requests.

Apply this standard:
1) Always use a hard bound: attach an AbortSignal (and/or explicit timeout) to every network call that could otherwise hang. Don’t rely on implicit/idle behavior.
2) Preserve routing/proxy semantics: if you override the HTTP dispatcher/agent (for timeouts, keep-alive, etc.), keep loopback behavior direct when proxies are set (e.g., HTTP_PROXY without NO_PROXY must not break localhost). Also gate “local server” behavior using robust local-network detection (handle 0.0.0.0 and mapped IPv4).
3) Make retry logic dispatch-aware: when a transport spans reconnects, separate “queued/unsent” from “dispatched/accepted”. Only offer “resend” when you have a definitive pre-dispatch failure; suppress or withdraw resends after detach/forget/confirmed dispatch to prevent duplicate side effects.

Example (timeout + abort-bound fetch):
```ts
async function fetchWithTimeout(input: RequestInfo, init: RequestInit) {
  const controller = new AbortController();
  const t = setTimeout(() => controller.abort(new Error("timeout")), 5000);
  try {
    return await fetch(input, { ...init, signal: controller.signal });
  } finally {
    clearTimeout(t);
  }
}
```

Example (don’t resend without dispatch certainty):
```ts
// Pseudocode for hub/transport clients
const result = await hub.send(prompt);
if (result.dispatched) {
  // Don’t resend; treat as accepted and wait for delivery/ack.
} else if (result.preDispatchFailureConfirmed) {
  // Safe to surface “resend draft” to user.
} else {
  // Lost/ambiguous: suppress resend UI until delivery state is known.
}
```