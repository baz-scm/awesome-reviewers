---
title: Bounded Proxy-Correct Fetch
description: 'For any HTTP request, especially long-running streaming/generation calls:
  (1) choose the correct fetch/dispatcher for the target (local vs remote), while
  preserving loopback/direct routing semantics under proxies; (2) ensure every code
  path—including fallbacks—has the same AbortSignal/timeout budget.'
repository: cline/cline#v19
label: Networking
language: TypeScript
comments_count: 3
repository_stars: 70885
---

For any HTTP request, especially long-running streaming/generation calls: (1) choose the correct fetch/dispatcher for the target (local vs remote), while preserving loopback/direct routing semantics under proxies; (2) ensure every code path—including fallbacks—has the same AbortSignal/timeout budget.

Application rules
- Proxy/loopback correctness: if your app uses env-var proxies (e.g., HTTP_PROXY) via an undici Agent/dispatcher, explicitly preserve “direct connect to loopback” behavior (e.g., when HTTP_PROXY is set but NO_PROXY is absent). Add a regression test for the loopback case.
- Local-network targeting: if you route to a special fetch (e.g., disabling idle timeouts), make sure your “local” detection covers common variants like 0.0.0.0 and IPv4-mapped loopback addresses; otherwise you’ll silently fall back to the default timeouts.
- No unbounded fallback: never let a fallback path use a bare fetch. Thread through the caller’s AbortSignal (or implement a timeout wrapper) so hangs don’t prevent tasks from starting.

Example pattern
```ts
import { Agent, EnvHttpProxyAgent } from "undici";

const noIdleTimeoutAgent = new EnvHttpProxyAgent({ headersTimeout: 0, bodyTimeout: 0 });
const loopbackAgent = new Agent({ headersTimeout: 0, bodyTimeout: 0 });

function isLoopback(url: URL) {
  return url.hostname === "localhost" || url.hostname === "127.0.0.1" || url.hostname === "::1";
}

export async function fetchWithBudget(
  url: string,
  init: RequestInit & { abortSignal?: AbortSignal },
  budgetMs: number,
) {
  const ac = new AbortController();
  const signal = init.abortSignal;
  if (signal) {
    signal.addEventListener("abort", () => ac.abort(signal.reason), { once: true });
  }
  const t = setTimeout(() => ac.abort(new Error(`timeout ${budgetMs}ms`)), budgetMs);

  try {
    const u = new URL(url);
    const dispatcher = isLoopback(u) ? loopbackAgent : noIdleTimeoutAgent;
    return await fetch(url, { ...init, dispatcher, signal: ac.signal });
  } finally {
    clearTimeout(t);
  }
}
```

This prevents (a) proxy-driven regressions for localhost, (b) undici idle-timeout failures for long local generation, and (c) hangs caused by unbounded fallback fetches.