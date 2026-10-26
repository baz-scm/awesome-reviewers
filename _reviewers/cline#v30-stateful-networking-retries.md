---
title: Stateful Networking Retries
description: 'Networking reliability should be implemented as an explicit, stateful
  protocol: separate “prepared”, “dispatched (sent over the wire)”, and “failed before
  dispatch”, and then make retry/resend UI and logic depend on that boundary.'
repository: cline/cline#v30
label: Networking
language: TypeScript
comments_count: 7
repository_stars: 70894
---

Networking reliability should be implemented as an explicit, stateful protocol: separate “prepared”, “dispatched (sent over the wire)”, and “failed before dispatch”, and then make retry/resend UI and logic depend on that boundary.

Apply these rules:
- **Record dispatch boundary**: Require the transport/hub layer to return (or emit) a signal like `dispatched: true/false` or a typed failure variant that tells whether the message was actually sent.
- **Only resend pre-dispatch failures**: If the boundary says it was already dispatched, do **not** offer resend; recovery must treat it as “maybe delivered” and avoid duplicate sends.
- **Track in-flight operations**: For hub/lease-style commands (attachments, invocations), keep per-session in-flight markers so reconnect retries don’t re-attach twice.
- **Bound every request**: Always pass an `AbortSignal` (or use explicit timeouts) for both primary requests and fallback paths; unbounded fallbacks can stall startup.
- **Make routing deterministic for localhost**: When using proxy-aware HTTP agents, preserve loopback direct routing and correctly detect local addresses (including `0.0.0.0` and IPv4-mapped loopback) so local model servers don’t get sent through a proxy.

Illustrative pattern (dispatch-bound retry):
```ts
async function sendWithNoDoubleDispatch(sendFn: () => Promise<{ dispatched: boolean }>) {
  try {
    const res = await sendFn();
    return { ok: true, dispatched: res.dispatched };
  } catch (e: any) {
    const dispatched = e?.dispatched === true;
    if (dispatched) {
      // Already on the wire: never auto-resend.
      return { ok: false, dispatched, action: "wait_or_check_status" };
    }
    // Pre-dispatch failure: safe to retry or offer resend.
    return { ok: false, dispatched: false, action: "retry_or_resend" };
  }
}
```

This standard prevents duplicate sends after transport recovery, avoids infinite network hangs from unbounded fallbacks, and keeps localhost/proxy behavior consistent.