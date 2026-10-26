---
title: Stateful Network Dispatch
description: Network code should behave deterministically across retries/reconnects
  by (a) confirming exactly when data is accepted/“dispatched”, (b) preventing duplicate
  sends, and (c) bounding/aborting all network work.
repository: Cline/Cline
label: Networking
language: TypeScript
comments_count: 7
repository_stars: 70840
---

Network code should behave deterministically across retries/reconnects by (a) confirming exactly when data is accepted/“dispatched”, (b) preventing duplicate sends, and (c) bounding/aborting all network work.

Apply this as a checklist:
1) **Use an explicit dispatch/acceptance boundary**
   - Only treat failures as “unsent” (eligible for resend/UI replay) if you can confirm the payload was *not* dispatched to the transport.
   - If the hub/client can’t provide that signal, add one (return value/event/hook) and plumb it through typed errors.

2) **Make retries safe with in-flight tracking**
   - When reconnecting or re-registering, track which operations are still awaiting a reply and skip re-sending those to avoid duplicate side effects (e.g., attaches).

3) **Bound and abort every network path**
   - Ensure *all* fetch/socket code paths—including fallbacks—use an AbortSignal and a timeout. Avoid “bare fetch” fallbacks that can hang indefinitely.

4) **Preserve intended routing for local services under proxies**
   - When you add custom dispatchers (e.g., to disable idle timeouts), ensure loopback/local addresses still bypass proxies when required (test with `HTTP_PROXY` set and `NO_PROXY` unset).

Minimal pattern (dispatch boundary + resend gating):
```ts
type SendFailure =
  | { kind: "preDispatch"; unsentPrompt: string }
  | { kind: "postDispatch"; warning?: string };

async function sendWithSafeReplay(hub: HubClient, payload: string): Promise<void> {
  const result = await hub.send({ payload });
  // result must include whether transport accepted the dispatch boundary
  // e.g. { dispatched: true } or a typed failure with pre/postDispatch.

  if (result.ok) return;

  if (result.failure.kind === "preDispatch") {
    // eligible: UI can offer the unsent draft for retry
    throw new Error(`Pre-dispatch failed; can retry draft: ${result.failure.unsentPrompt}`);
  }

  // not eligible: the transport may have already sent; do not offer replay
  throw new Error("Post-dispatch failure; do not resend to avoid duplicates");
}
```

Concrete outcomes you should see after adopting this:
- No double-send/double-attach from transport retries.
- No “hung” starts due to unbounded fallback requests.
- Local model/proxy setups continue to work (loopback routing preserved) while remote traffic still uses the proxy-aware path.
- Viewer/session reads wait briefly for connection readiness rather than failing immediately when the transport is still connecting.