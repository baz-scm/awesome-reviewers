---
title: Reliable Network Retries
description: 'When implementing networked features (hub dispatch, reconnect/reattach,
  model/catalog fetches, and local-proxy HTTP), ensure retries are safe and bounded:'
repository: CLINE/cline
label: Networking
language: TypeScript
comments_count: 6
repository_stars: 70839
---

When implementing networked features (hub dispatch, reconnect/reattach, model/catalog fetches, and local-proxy HTTP), ensure retries are safe and bounded:

- **Model the dispatch boundary/ack:** if a send may fail after it was dispatched, surface that fact and **only offer resend for confirmed pre-dispatch failures**. Prevent “double-send” UIs.
- **Be connection-state aware:** during `connecting`, prefer **bounded wait + retry** for reads (e.g., transcript/status) instead of failing immediately.
- **Apply timeouts + AbortSignal everywhere (including fallbacks):** never use an unbounded `fetch`/socket call as a fallback path; propagate the same abort logic.
- **Make routing explicit for local/loopback:** when using proxy-aware dispatchers, preserve direct routing for loopback/local addresses and correctly classify common local bind targets (e.g., `0.0.0.0`, IPv4-mapped loopback).

Example pattern (safe resend + bounded, abortable requests):

```ts
async function sendWithSafeRetry(params: {
  attemptId: string;
  sessionId: string;
  send: () => Promise<{ dispatched: boolean; error?: { code?: string } }>;
  onProgress: (msg: string) => void;
  abortSignal: AbortSignal;
  timeoutMs: number;
}) {
  const { send, timeoutMs, abortSignal } = params;

  const controller = new AbortController();
  const t = setTimeout(() => controller.abort(), timeoutMs);
  abortSignal.addEventListener("abort", () => controller.abort(), { once: true });

  try {
    params.onProgress("sending");
    const { dispatched, error } = await send();

    if (!dispatched) {
      // Safe to retry / re-offer draft only for pre-dispatch failures.
      // If you retry here, ensure you don’t exceed UX expectations.
      if (error?.code === "transport_error") {
        params.onProgress("retrying");
        return await send();
      }
    }

    return { dispatched, error };
  } finally {
    clearTimeout(t);
  }
}
```

Use the same principles for:
- hub attach/invoke resend after reconnect (tie resend eligibility to dispatch/lease state),
- transcript/status reads that should wait for hub link connection,
- primary+fallback HTTP fetches (primary errors must not trigger an unbounded, non-abortable fallback),
- local model routing under proxy environments (loopback/direct must stay direct, and local-address detection must include real-world bind patterns).