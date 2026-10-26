---
title: Proxy and Abort Discipline
description: 'When code changes networking behavior (proxy routing, local-vs-remote
  handling, or timeouts), enforce two invariants everywhere:


  1) **Preserve direct loopback behavior even under HTTP proxy env vars.** If a host
  is loopback/local in your product’s routing model, it must bypass proxy CONNECT/dial
  paths; otherwise previously working local servers (e.g., LM...'
repository: cline/cline#v12
label: Networking
language: TypeScript
comments_count: 5
repository_stars: 70872
---

When code changes networking behavior (proxy routing, local-vs-remote handling, or timeouts), enforce two invariants everywhere:

1) **Preserve direct loopback behavior even under HTTP proxy env vars.** If a host is loopback/local in your product’s routing model, it must bypass proxy CONNECT/dial paths; otherwise previously working local servers (e.g., LM Studio/Ollama) will fail when users set `HTTP_PROXY` without `NO_PROXY`.

2) **Never leave an unbounded fallback path.** Every request path—including “fallback” calls—must use the same `AbortSignal`/deadline/dispatcher policy as the primary call. Otherwise retries time out while fallbacks hang and block startup/flows.

3) **Parameterize reachability/policy.** If behavior depends on explicit connection/binding settings, let caller-supplied options win and gate network-policy rules consistently across platforms (e.g., sandbox/policy tiers).

Practical pattern:
```ts
// Example: share AbortSignal + split loopback vs proxied routing.
export function makeFetch(config: {
  loopbackHosts: (hostname: string) => boolean;
  createLoopbackAgent: () => Agent;
  createProxyAgent: () => Agent;
}) {
  return async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = typeof input === "string" || input instanceof URL ? new URL(input) : new URL(input.url);
    const agent = config.loopbackHosts(url.hostname)
      ? config.createLoopbackAgent()
      : config.createProxyAgent();

    return fetchWithDispatcher(input, {
      ...init,
      // Ensure the same AbortSignal/timeout is used for PRIMARY + FALLBACK paths.
      signal: init?.signal,
      dispatcher: agent,
    });
  };
}

async function fetchWithFallback(primary: () => Promise<any>, fallback: () => Promise<any>, signal: AbortSignal) {
  try {
    return await primary();
  } catch (e) {
    // Critical: fallback must also accept/use the same AbortSignal/deadline.
    return await fallback();
  }
}
```

Checklist for code review:
- For each network request call site: Is the dispatcher/agent selection correct for loopback/local vs remote under `HTTP_PROXY`?
- Do **all** branches (fallbacks, retries, secondary lookups) use the same `AbortSignal`/timeout/deadline?
- Are network-policy decisions (local subnet allowlists, sandbox ingress/egress, bind fallback) explicit, parameterized, and tested for platform/proxy combinations?
- Are there regression tests for the known “break in production” setup (e.g., `HTTP_PROXY` set + `NO_PROXY` unset + loopback model server)?
