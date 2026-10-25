---
title: Proxy And Timeout Discipline
description: 'When you customize networking (HTTP agents, proxy dispatchers, sandboxes,
  or long-running requests), follow these rules:


  1) Preserve loopback/direct routing semantics'
repository: ClInE/cLiNe
label: Networking
language: TypeScript
comments_count: 4
repository_stars: 70838
---

When you customize networking (HTTP agents, proxy dispatchers, sandboxes, or long-running requests), follow these rules:

1) Preserve loopback/direct routing semantics
- If your environment may set HTTP(S)_PROXY and NO_PROXY is absent, do not rely on a proxy agent to route localhost/127.0.0.1/::1 directly; explicitly preserve “direct to loopback” behavior.
- Add a regression test that runs with HTTP_PROXY set and NO_PROXY unset and verifies loopback reaches the local server.

2) Guarantee cancellation/termination for all request paths
- Every network call—including fallbacks—must honor the request AbortSignal and/or have a bounded timeout.
- Watch for “fallback uses bare fetch” patterns; they should pass through the same AbortSignal and have consistent caps, especially for operations that must complete before a task starts.

3) Handle disconnect/cancellation consistently
- For socket-based workflows, avoid immediately cancelling in-flight work on transient disconnects unless that’s the explicit policy. Consider a short grace period for already-pending requests where it improves user experience/consistency.

4) Keep platform-specific network/sandbox policies compatible
- If a sandbox enforcement tier fails on a policy (e.g., loopback ingress on a Windows MXC fallback), gate those network policy flags by platform/feature availability so networking doesn’t become non-functional.

Example pattern (HTTP agent + preserved loopback + AbortSignal):

```ts
import { fetch as undiciFetch, Agent as HttpAgent } from "undici";

const loopbackAgent = new HttpAgent({ headersTimeout: 0, bodyTimeout: 0 });

export function makeFetchWithTimeouts(
  agentForRemote: any, // your proxy-aware agent
) {
  return async function fetchWithPolicy(input: RequestInfo | URL, init: RequestInit = {}) {
    const url = typeof input === "string" ? new URL(input) : new URL(input.toString());

    // Preserve direct loopback routing even when HTTP_PROXY is set.
    const isLoopback = url.hostname === "localhost" || url.hostname === "127.0.0.1" || url.hostname === "::1";
    const dispatcher = isLoopback ? loopbackAgent : agentForRemote;

    // Ensure cancellation applies to *all* paths, including fallbacks.
    // (Also apply a bounded timeout via AbortController if needed.)
    return undiciFetch(url, {
      ...init,
      dispatcher,
      signal: init.signal,
    });
  };
}
```

Apply this standard anywhere you touch HTTP dispatchers/agents, retry/fallback logic, or socket disconnect handling—so local models still work under proxies, requests don’t hang indefinitely, and network policy doesn’t accidentally break sandboxing.