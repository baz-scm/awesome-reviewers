---
title: Bound Network Requests
description: Ensure every network request is (a) correctly routed with respect to
  proxy settings—especially for loopback—and (b) bounded/abortable so packet-drop
  or stalled connections can’t hang execution. Also make local-server detection robust
  so you apply the right transport/timeouts for localhost vs remote.
repository: cline/cline#v7
label: Networking
language: TypeScript
comments_count: 3
repository_stars: 70865
---

Ensure every network request is (a) correctly routed with respect to proxy settings—especially for loopback—and (b) bounded/abortable so packet-drop or stalled connections can’t hang execution. Also make local-server detection robust so you apply the right transport/timeouts for localhost vs remote.

Apply this standard:
- Never use a “bare” fetch/HTTP call as a fallback without an AbortSignal/timeout.
- When using custom undici/fetch dispatchers/agents, preserve the “always direct to loopback” behavior even if HTTP_PROXY is set and NO_PROXY is absent.
- When choosing special handling for “local model servers,” correctly classify common local bind addresses like 0.0.0.0 and IPv4-mapped loopback (::ffff:127.0.0.1), not just 127.0.0.1/::1.
- Add a regression test that runs with HTTP_PROXY set and NO_PROXY unset to verify loopback still connects directly.

Example pattern:
```ts
import { EnvHttpProxyAgent } from "undici";

const proxyAgent = new EnvHttpProxyAgent({ headersTimeout: 0, bodyTimeout: 0 });
const directAgent = /* a plain Agent/dispatcher that connects directly */ undefined;

function isLoopbackHost(host: string): boolean {
  return host === "localhost" || host === "127.0.0.1" || host === "::1";
}

export async function fetchWithAbort(input: string | URL, init?: RequestInit) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 10_000);
  try {
    const url = typeof input === "string" ? new URL(input) : input;
    const isLoopback = isLoopbackHost(url.hostname);

    return await fetch(url, {
      ...init,
      dispatcher: isLoopback ? directAgent : proxyAgent,
      signal: init?.signal ?? controller.signal,
    });
  } finally {
    clearTimeout(timeoutId);
  }
}
```
Use the same bounded/abortable wrapper for both primary requests and any fallback paths (e.g., model discovery fallbacks).