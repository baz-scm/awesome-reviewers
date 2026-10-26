---
title: Connection-Aware Networking
description: 'Treat networking as a stateful, failure-prone protocol: code should
  wait for readiness (with bounds), classify failures by whether the operation was
  dispatched, and ensure every network path (including fallbacks) is cancellation/timeout
  correct—while remaining correct under proxy/local-network conditions.'
repository: cline/cline#v22
label: Networking
language: TypeScript
comments_count: 6
repository_stars: 70886
---

Treat networking as a stateful, failure-prone protocol: code should wait for readiness (with bounds), classify failures by whether the operation was dispatched, and ensure every network path (including fallbacks) is cancellation/timeout correct—while remaining correct under proxy/local-network conditions.

Apply these rules:
1) **Readiness wait + bounded retry for dependent connections**
- When you depend on a socket/link that may still be connecting, wait briefly for “connected” before the first read.
- If a disconnect occurs, retry once after reconnection; if the operation still can’t be performed, return an explicit failure state (e.g., `"unknown"`) rather than an empty/default success.

2) **Dispatch-aware retries/resends**
- Any UI/logic that offers “resend” must be gated by whether the prompt/request was actually dispatched over the transport.
- If the client cannot confirm dispatch, only allow resend for *confirmed pre-dispatch* failures; treat “lost reply” separately (don’t replay automatically).

3) **End-to-end cancellation/timeout coverage**
- Ensure the same `AbortSignal` (or equivalent timeout) is used across the entire code path, including fallbacks.
- Avoid “primary bounded, fallback unbounded” patterns that can stall background tasks.

4) **Proxy/local-network correctness with regression tests**
- If you introduce fetch/dispatcher wrappers (e.g., to disable idle timeouts for local model servers), preserve loopback/direct-routing semantics under `HTTP_PROXY`/`NO_PROXY`.
- Gate the wrapper based on robust local-network address classification, including edge cases like `0.0.0.0` and IPv4-mapped IPv6.
- Add regression tests for proxy+no-proxy behavior.

Example (pattern sketch):
```ts
async function safeHubTranscript(link: { connected: (ms: number) => Promise<boolean>, command: Function }, sessionId: string) {
  const connected = await link.connected(5000);
  if (!connected) return { messages: [], status: "unknown" };

  const reply = await link.command("session.messages", { sessionId }).catch(() => undefined);
  if (!reply) {
    // One reconnect retry pattern
    const reconnected = await link.connected(5000);
    if (reconnected) {
      return await link.command("session.messages", { sessionId }).catch(() => ({ messages: [], status: "unknown" }));
    }
    return { messages: [], status: "unknown" };
  }
  return reply;
}
```

This standard prevents “instant failures while connecting”, avoids duplicate side effects from unsafe retries, ensures cancellations actually stop all network branches, and keeps networking behavior correct across real-world proxy + local-server setups.