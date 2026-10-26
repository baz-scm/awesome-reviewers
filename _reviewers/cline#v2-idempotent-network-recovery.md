---
title: Idempotent Network Recovery
description: When connectivity is unstable (disconnects, endpoint-not-ready, hub reconnects),
  your networking layer must preserve *in-flight* intent and prevent *double execution*.
repository: cline/cline#v2
label: Networking
language: TypeScript
comments_count: 5
repository_stars: 70861
---

When connectivity is unstable (disconnects, endpoint-not-ready, hub reconnects), your networking layer must preserve *in-flight* intent and prevent *double execution*.

Apply these rules:
1) Distinguish **pre-dispatch vs post-dispatch** failures. Your code/UI must know whether the hub/transport already sent the request. If it dispatched, do not allow a resend that would duplicate the operation.
2) For pending operations during transient disconnects, prefer **reconnect grace** over immediate cancel. Keep the same pending request and its callback/state; only cancel on grace expiry or explicit stop/detach.
3) For “connection not ready”, **hold the command open** until the transport becomes ready (within a deadline). Avoid failing immediately on the first refusal.
4) Use **bounded retries/ready-waits** for hub/transport reads: wait for connection to be established for a short window, then return a meaningful status.
5) Ensure every critical network path—*including fallbacks*—is **abortable** via the same AbortSignal/timeout budget as the primary call.

Example pattern (sketch):
```ts
type SendOutcome =
  | { dispatched: true }
  | { dispatched: false; error: unknown };

async function sendWithDispatchBoundary(hub, request, abortSignal): Promise<SendOutcome> {
  // Hub must return whether/when it crossed the dispatch boundary.
  return hub.send(request, { abortSignal });
}

async function maybeResend(outcome: SendOutcome, uiCanRetry: boolean) {
  // Only allow retry when we *know* we did not dispatch.
  if (!uiCanRetry) return;
  if (outcome.dispatched) return; // already sent; never auto-resend
  // pre-dispatch failure: safe to offer resend
}
```

If you implement (1) dispatch-boundary reporting and (2) pending-request preservation with reconnect grace, the rest of the behaviors (wait-for-ready, hold commands, retry-with-deadlines, and abortable fallbacks) become straightforward and testable.