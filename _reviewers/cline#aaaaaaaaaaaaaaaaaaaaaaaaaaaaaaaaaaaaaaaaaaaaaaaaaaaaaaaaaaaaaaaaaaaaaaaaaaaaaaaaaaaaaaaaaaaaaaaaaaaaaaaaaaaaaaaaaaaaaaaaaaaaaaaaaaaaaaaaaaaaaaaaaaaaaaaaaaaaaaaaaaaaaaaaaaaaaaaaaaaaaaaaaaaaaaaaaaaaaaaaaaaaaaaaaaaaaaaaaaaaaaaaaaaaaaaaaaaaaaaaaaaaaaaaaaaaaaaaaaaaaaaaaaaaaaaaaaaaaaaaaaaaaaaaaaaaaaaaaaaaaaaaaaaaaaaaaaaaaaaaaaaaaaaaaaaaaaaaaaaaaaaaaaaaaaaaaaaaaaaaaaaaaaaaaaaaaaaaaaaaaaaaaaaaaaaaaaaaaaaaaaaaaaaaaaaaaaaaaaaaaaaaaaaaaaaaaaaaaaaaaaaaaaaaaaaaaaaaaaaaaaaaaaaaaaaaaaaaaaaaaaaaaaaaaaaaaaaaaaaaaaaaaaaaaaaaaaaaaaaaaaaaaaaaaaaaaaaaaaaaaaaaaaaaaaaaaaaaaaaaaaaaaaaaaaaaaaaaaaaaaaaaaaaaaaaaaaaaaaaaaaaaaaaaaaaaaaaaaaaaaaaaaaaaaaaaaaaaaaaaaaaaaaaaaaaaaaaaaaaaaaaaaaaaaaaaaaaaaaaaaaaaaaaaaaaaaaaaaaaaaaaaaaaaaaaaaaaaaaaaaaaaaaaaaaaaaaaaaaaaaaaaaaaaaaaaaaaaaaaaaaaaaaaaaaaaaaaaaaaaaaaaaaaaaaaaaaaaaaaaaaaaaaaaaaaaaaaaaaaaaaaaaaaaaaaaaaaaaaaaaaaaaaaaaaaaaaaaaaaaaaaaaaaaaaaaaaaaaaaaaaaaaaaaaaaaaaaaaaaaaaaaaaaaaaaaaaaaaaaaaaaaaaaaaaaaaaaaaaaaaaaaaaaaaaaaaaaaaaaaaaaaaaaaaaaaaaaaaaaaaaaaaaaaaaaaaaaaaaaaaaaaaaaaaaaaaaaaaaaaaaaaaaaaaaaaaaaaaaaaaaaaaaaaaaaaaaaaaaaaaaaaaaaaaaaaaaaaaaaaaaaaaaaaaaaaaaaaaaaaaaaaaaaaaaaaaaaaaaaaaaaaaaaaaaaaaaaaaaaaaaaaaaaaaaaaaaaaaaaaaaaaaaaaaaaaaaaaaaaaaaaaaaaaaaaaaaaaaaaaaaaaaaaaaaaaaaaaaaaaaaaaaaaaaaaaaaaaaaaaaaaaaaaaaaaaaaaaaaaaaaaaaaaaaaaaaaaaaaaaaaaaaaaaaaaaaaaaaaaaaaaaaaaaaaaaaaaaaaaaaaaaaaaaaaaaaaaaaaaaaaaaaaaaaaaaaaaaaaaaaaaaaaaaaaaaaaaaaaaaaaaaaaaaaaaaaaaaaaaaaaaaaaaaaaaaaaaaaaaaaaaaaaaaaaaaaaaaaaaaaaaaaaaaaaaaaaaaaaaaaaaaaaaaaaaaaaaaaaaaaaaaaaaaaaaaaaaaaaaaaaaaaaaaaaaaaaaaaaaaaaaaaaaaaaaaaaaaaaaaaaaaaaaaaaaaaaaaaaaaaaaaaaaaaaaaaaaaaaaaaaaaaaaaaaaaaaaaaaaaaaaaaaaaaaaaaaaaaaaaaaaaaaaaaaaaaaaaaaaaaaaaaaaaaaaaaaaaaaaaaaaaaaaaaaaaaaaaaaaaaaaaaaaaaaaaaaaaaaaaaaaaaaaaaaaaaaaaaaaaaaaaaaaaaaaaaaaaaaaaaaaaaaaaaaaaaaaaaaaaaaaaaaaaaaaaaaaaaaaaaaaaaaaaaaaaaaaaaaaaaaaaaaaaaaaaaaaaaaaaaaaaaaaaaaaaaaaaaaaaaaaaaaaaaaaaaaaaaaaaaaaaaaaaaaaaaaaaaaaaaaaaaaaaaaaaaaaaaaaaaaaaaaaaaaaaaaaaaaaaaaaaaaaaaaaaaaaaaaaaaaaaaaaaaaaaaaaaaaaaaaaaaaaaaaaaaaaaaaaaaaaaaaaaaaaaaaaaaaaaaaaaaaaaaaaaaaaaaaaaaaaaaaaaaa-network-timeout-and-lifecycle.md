---
title: Network timeout and lifecycle
description: Every outbound network call must have an explicit, enforced bound on
  how long it can hang, and connection state must be validated or invalidated before
  reuse so stale sockets or credentials never silently cause failures or hangs.
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Networking
language: TypeScript
comments_count: 7
repository_stars: 70970
---

Every outbound network call must have an explicit, enforced bound on how long it can hang, and connection state must be validated or invalidated before reuse so stale sockets or credentials never silently cause failures or hangs.

Concretely:
- Never issue a network request without a timeout/cancellation mechanism. Prefer `AbortSignal.timeout(ms)`, but if the callee is caller-supplied (e.g. a host-provided fetch) or otherwise might ignore the signal, add a defensive backstop timer that rejects the pending promise so one hung call can't block startup or task execution (e.g. `createComposioMetaToolSession`'s extra deadline timer, and the missing timeout on `fetchModelIdsFromSource`'s fallback fetch that can hang a task start).
- Apply timeouts consistently to all code paths, including fallbacks — a bounded primary request with an unbounded fallback still produces a hang.
- Before retrying or reusing a connection, close/invalidate any stale resource first (e.g. close a `CONNECTING` socket before `retryConnection`, close the SSH control master and drop its cached control path when identity/credentials change) so retries don't race against or silently reuse a dead/incorrect connection.
- When a command or request appears to time out, don't immediately tear down a healthy transport. Use a lightweight, coalesced health probe (e.g. a bounded `client.list` ping) to distinguish a genuinely dead connection from one slow reply; only retire the transport if the probe also fails. Never replay non-idempotent writes based solely on a timeout.
- When building proxy/routing logic (e.g. `EnvHttpProxyAgent`), explicitly handle loopback/localhost addresses to bypass the proxy, matching the platform's existing direct-connection behavior, and add regression tests with `HTTP_PROXY` set and `NO_PROXY` unset to catch accidental proxying of local servers.

Example pattern for defensive timeout on a caller-supplied transport:
```ts
const pendingResponse = request(url, { signal: AbortSignal.timeout(TIMEOUT_MS) });
const deadline = new Promise<never>((_, reject) => {
  const timer = setTimeout(() => reject(new Error("request deadline exceeded")), TIMEOUT_MS + GRACE_MS);
  pendingResponse.finally(() => clearTimeout(timer));
});
const response = await Promise.race([pendingResponse, deadline]);
```</description>
