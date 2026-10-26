---
title: Stateful network lifecycle
description: 'For any network operation that can be pending (requests, websocket commands,
  streaming), explicitly define—and test—the lifecycle rules for: connection state,
  grace periods, deadlines, cancellation, and terminal events. Avoid “best-effort”
  retries that don’t match actual transport state.'
repository: cline/cline#v18
label: Networking
language: TypeScript
comments_count: 6
repository_stars: 70884
---

For any network operation that can be pending (requests, websocket commands, streaming), explicitly define—and test—the lifecycle rules for: connection state, grace periods, deadlines, cancellation, and terminal events. Avoid “best-effort” retries that don’t match actual transport state.

Checklist
- Model states (e.g., connecting/unavailable/connected) and ensure retry UI/logic is reachable in the same states where retries are meaningful.
- On disconnect: either preserve in-flight work for a defined grace window and cancel only when the grace expires, or cancel immediately—but make it consistent with user intent (don’t silently change behavior).
- On commands: keep them pending through transient “endpoint not ready” failures; fail only after the explicit connect deadline. Add assertions that the command is still pending before the deadline midpoint, not just that it eventually fails.
- On long-running local HTTP: use environment-aware routing and timeout settings (e.g., bypass loopback when `HTTP_PROXY` is set and `NO_PROXY` isn’t) and disable idle timeouts only for the intended local-network providers.
- On streaming: treat “finish/stop” conditions according to lifecycle rules; don’t close sockets or stop the microphone based on provider events that can occur under other commit strategies.

Illustrative pattern (command pending across transient failures)
```ts
// Pseudocode: keep one in-flight command pending until grace/deadline.
const inFlight = new Map<string, {promise, resolve, reject, startedAt}>();

function sendCommand(key: string, sendOverSocket: () => void, deadlineMs: number, graceMs: number) {
  const existing = inFlight.get(key);
  if (existing) return existing.promise;

  const promise = new Promise((resolve, reject) => {
    const startedAt = Date.now();
    const timeout = setTimeout(() => {
      if (Date.now() - startedAt >= deadlineMs) reject(new Error('connect deadline passed'));
    }, deadlineMs);

    const trySend = () => {
      // If socket disconnects, retry sending only after grace expiry expires.
      // Do not re-execute callbacks; just re-send the command once the endpoint is ready.
      sendOverSocket();
    };

    // Subscribe to connection readiness; call trySend when ready.
  });

  inFlight.set(key, {promise, resolve: null, reject: null, startedAt: Date.now()});
  return promise.finally(() => inFlight.delete(key));
}
```

Rule of thumb: if users can hit “Stop,” or if the code has UI for “Retry,” then the network code must have deterministic state transitions and tests for both (a) what happens before grace/deadline expiry and (b) what happens after.