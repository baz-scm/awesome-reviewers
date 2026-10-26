---
title: Deterministic Network Lifecycle
description: 'When implementing networking (hub/transport, retries, retries after
  reconnect, and custom fetch), make request lifecycle *explicit* and *bounded*.


  **Rules**'
repository: cline/cline#x
label: Networking
language: TypeScript
comments_count: 6
repository_stars: 70861
---

When implementing networking (hub/transport, retries, retries after reconnect, and custom fetch), make request lifecycle *explicit* and *bounded*.

**Rules**
1) **Track dispatch boundary to prevent double-send**
- Network code must know whether a message was dispatched to the peer (or hub) versus only queued locally.
- Retry/resend UI logic must only offer resend for **pre-dispatch** failures.

2) **Maintain pending requests through transient disconnects (or cancel deterministically)**
- If behavior changes across disconnect, either:
  - keep the same pending request until a reconnect grace/deadline expires, or
  - cancel immediately—but then don’t later present it as safely retryable without state guarantees.

3) **Use in-flight tracking for connection-bound operations**
- When resending after reconnect/registration, keep separate state for:
  - remembered-but-not-sent operations, and
  - operations already sent/in-flight (so they aren’t duplicated).

4) **All fetches must be abortable and time-bounded**
- Ensure every fallback path (including “helper” discovery calls) uses an `AbortSignal` and a timeout.
- Never rely on implicit runtime network timeouts.

5) **Preserve correct routing for local endpoints**
- If you customize HTTP agents/fetch, ensure loopback/local routing remains direct when `NO_PROXY` semantics would otherwise bypass proxies; add tests with `HTTP_PROXY` set and `NO_PROXY` unset.

**Sketch pattern (dispatch boundary + safe resend)**
```ts
type SendResult =
  | { dispatched: true }
  | { dispatched: false; error: unknown };

async function sendWithDispatchSignal(...): Promise<SendResult> {
  // pre-dispatch: enqueue/prepare only
  // dispatch: after hub/transport acknowledges it crossed the boundary
  try {
    const dispatched = await transport.send(...); // return boundary signal
    return dispatched
      ? { dispatched: true }
      : { dispatched: false, error: new Error('not dispatched') };
  } catch (e) {
    // classify: if e occurred before boundary => dispatched=false
    return { dispatched: false, error: e };
  }
}

function uiResendAllowed(result: SendResult) {
  // Only allow resend when nothing reached the peer.
  return !result.dispatched;
}
```

Apply these rules to hub/transport messaging, reconnect/re-registration flows, and provider HTTP fetches to avoid duplicated actions, hanging requests, and environment-specific networking regressions.