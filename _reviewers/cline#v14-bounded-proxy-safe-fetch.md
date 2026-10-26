---
title: Bounded, Proxy-Safe Fetch
description: When making HTTP requests in networking-sensitive code, ensure (1) every
  network path is bounded (timeouts and/or AbortSignal), and (2) proxy/loopback behavior
  is correct and consistent with existing routing expectations.
repository: cline/cline#v14
label: Networking
language: TypeScript
comments_count: 3
repository_stars: 70876
---

When making HTTP requests in networking-sensitive code, ensure (1) every network path is bounded (timeouts and/or AbortSignal), and (2) proxy/loopback behavior is correct and consistent with existing routing expectations.

Apply these rules:
- Never leave a fallback (secondary code path) doing an unbounded `fetch`; always pass an `AbortSignal` and/or an explicit timeout.
- If you override fetch/agents for special behavior (e.g., disabling undici idle timeouts for local servers), preserve “direct-to-loopback” behavior when `HTTP_PROXY` is set: local/loopback traffic must bypass env-proxy CONNECT unless `NO_PROXY` explicitly matches.
- Make the “local address” decision robust (include 127.0.0.1, ::1, 0.0.0.0, and IPv4-mapped loopback) so the special-case fetch is applied correctly.
- Add regression tests that run with `HTTP_PROXY` set and `NO_PROXY` unset (verify loopback still reaches the server; a non-routable host fails appropriately).

Example pattern (self-contained):
```ts
import { setTimeout as delay } from "timers/promises";

function withTimeout(signal: AbortSignal | undefined, ms: number) {
  const c = new AbortController();
  const onAbort = () => c.abort(signal?.reason);
  if (signal) {
    if (signal.aborted) onAbort();
    else signal.addEventListener("abort", onAbort, { once: true });
  }
  const t = setTimeout(() => c.abort(new Error(`timeout after ${ms}ms`)), ms);
  c.signal.addEventListener("abort", () => clearTimeout(t), { once: true });
  return c.signal;
}

async function fetchAllPathsBounded(url: string, init: RequestInit & { signal?: AbortSignal }) {
  const boundedSignal = withTimeout(init.signal, 5000);

  const res = await fetch(url, { ...init, signal: boundedSignal });
  if (!res.ok) {
    // Fallback must also be bounded.
    return fetch(url + "/fallback", { ...init, signal: boundedSignal }).then(r => r.text());
  }
  return res.text();
}
```

Use this checklist before merging:
1) Do *all* request/fallback branches accept the same AbortSignal/timeout?
2) If an agent/dispatcher is customized, are loopback/local requests guaranteed to connect directly under `HTTP_PROXY`/`NO_PROXY`?
3) Is local address detection exhaustive enough to avoid accidental “remote behavior” for local servers?