---
title: Abortable Networking And Retries
description: 'Networking code must be resilient to disconnects/retries and safe for
  timeouts/cancellation, while preserving proxy/local routing invariants.


  Apply this standard:'
repository: cline/cline?x=1
label: Networking
language: TypeScript
comments_count: 7
repository_stars: 70861
---

Networking code must be resilient to disconnects/retries and safe for timeouts/cancellation, while preserving proxy/local routing invariants.

Apply this standard:
- **No unbounded requests in critical paths:** every HTTP fetch must be abortable (use an `AbortSignal`), and long-running operations must have explicit timeouts or cancellation wiring.
- **Cancellation must follow lifecycle state:** when connections drop or sessions are detached/forgotten/disposed, retries must not “re-lease” or continue work. Ensure re-dispatch hooks (or equivalent guards) run on both initial send and reconnect retry.
- **Reject stale commands after waiting:** if you defer execution until startup/transport settles, re-check that the originating connection/client is still active; otherwise fail fast instead of letting work continue on a dead connection.
- **Preserve proxy + locality rules when customizing HTTP behavior:** if you bypass idle timeouts for local model servers, still keep **loopback direct routing** semantics even when `HTTP_PROXY` is set and `NO_PROXY` is absent.
- **Be platform-aware for network/security policies:** sandbox/network policy flags that seem harmless (e.g., loopback ingress) may break protected execution on specific enforcement tiers.

Example (abortable fetch with local/loopback-aware dispatcher):
```ts
import { EnvHttpProxyAgent } from "undici";

const idleTimeoutFreeNoProxy = () => /* e.g. undici Agent with timeouts disabled and no proxy */ ({ /* ... */ });
const idleTimeoutFreeWithProxy = () => new EnvHttpProxyAgent({ headersTimeout: 0, bodyTimeout: 0 });

function isLoopback(hostname: string) {
  // implement robust checks: 127.0.0.0/8, ::1, 0.0.0.0 (if your provider uses it), mapped IPv4, etc.
  return hostname === "localhost" || hostname === "127.0.0.1" || hostname === "::1";
}

export async function fetchWithoutIdleTimeouts(url: string, init: RequestInit = {}) {
  const controller = init.signal ? null : new AbortController();
  const signal = init.signal ?? controller!.signal;

  const timeout = setTimeout(() => controller?.abort(new Error("timeout")), 30_000);
  try {
    const dispatcher = isLoopback(new URL(url).hostname)
      ? idleTimeoutFreeNoProxy()
      : idleTimeoutFreeWithProxy();

    return await fetch(url, { ...init, signal, dispatcher });
  } finally {
    clearTimeout(timeout);
  }
}
```

Use the same lifecycle/state checks for reconnect and retry paths as for initial sends, and treat every deferred/waited network operation as a potential stale-connection hazard.