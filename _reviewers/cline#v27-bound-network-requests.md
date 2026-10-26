---
title: Bound Network Requests
description: 'Ensure every outbound network operation has a clearly defined lifecycle:
  it must be (1) correctly routed (proxy vs loopback/local), (2) bounded (timeouts/AbortSignal)
  on all code paths including fallbacks, and (3) unambiguous about whether the payload
  was already dispatched so UI retry cannot double-send.'
repository: cline/cline#v27
label: Networking
language: TypeScript
comments_count: 5
repository_stars: 70892
---

Ensure every outbound network operation has a clearly defined lifecycle: it must be (1) correctly routed (proxy vs loopback/local), (2) bounded (timeouts/AbortSignal) on all code paths including fallbacks, and (3) unambiguous about whether the payload was already dispatched so UI retry cannot double-send.

Apply this standard:
1) Always bound network calls
- Wrap *every* HTTP fetch (primary and fallback) with the same AbortSignal you use for user “Stop”.
- Don’t leave fallback discovery paths with an unbounded fetch.

```ts
async function fetchWithAbort(input: RequestInfo | URL, init: RequestInit, signal: AbortSignal) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 10_000);
  signal.addEventListener('abort', () => controller.abort(), { once: true });
  try {
    return await fetch(input, { ...init, signal: controller.signal });
  } finally {
    clearTimeout(timer);
  }
}

// Use the same approach inside fallbacks.
```

2) Preserve intended proxy/loopback behavior
- If you introduce a special fetch/agent (e.g., to disable idle timeouts for local model servers), preserve the existing “loopback must bypass proxy” rule.
- Add regression tests covering HTTP_PROXY set and NO_PROXY unset.

3) Robustly classify “local server” targets
- Ensure your local-network gating handles common real-world variants: 0.0.0.0 and IPv4-mapped loopback (e.g., ::ffff:127.0.0.1). Otherwise you’ll silently fall back to the wrong fetch strategy and reintroduce idle-timeout failures.

4) Make dispatch/ack boundaries explicit to prevent double-send
- For hub/socket-based sends, rely on a transport-provided dispatch confirmation/boundary.
- Only present “resend” when the failure is confirmed to have occurred *before* dispatch; if dispatch may have happened, treat it as unconfirmed and avoid replay.

This combination prevents: request hangs on slow/unreachable local providers, proxy misrouting of localhost, incorrect timeout strategy selection, and duplicate network actions after partial failures or disconnects.