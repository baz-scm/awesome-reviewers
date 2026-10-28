---
title: Consistent timeouts and proxy routing
description: When customizing network behavior—timeouts, idle limits, or proxy routing—apply
  the change consistently across every code path a request can take, and never silently
  change existing connectivity guarantees.
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Networking
language: TypeScript
comments_count: 6
repository_stars: 70973
---

When customizing network behavior—timeouts, idle limits, or proxy routing—apply the change consistently across every code path a request can take, and never silently change existing connectivity guarantees.

- Bound every path, including fallbacks: if a primary request gets a timeout/AbortSignal, any fallback request triggered on its failure needs one too. A bare `fetch` with no timeout in a fallback can hang indefinitely even though the primary call is bounded, turning a quick failure into a stuck task.
- Preserve direct/loopback routing when introducing custom dispatchers or proxy-aware fetch variants. Don't let a general-purpose proxy agent (e.g. `EnvHttpProxyAgent`) route loopback or local-network addresses through a proxy if the platform's existing resolver always connects to them directly. Give loopback hosts a plain, no-timeout path and keep the proxy/env-aware agent only for non-local hosts.
- Cover every spelling of an address family when matching local/loopback ranges or building `NO_PROXY` exemptions: dotted-quad and `0.0.0.0`, IPv6 `::1`/`[::1]`, IPv4-mapped IPv6 (`::ffff:127.0.0.1`), and both casings of proxy env vars (`HTTP_PROXY`/`http_proxy`). Prefer address-aware utilities (e.g. `BlockList`) that normalize these instead of ad hoc string checks, and add regression tests with the proxy env vars actually set (not deleted) to catch regressions in the matching logic.
- Document and bound any intentional exception to timeouts rather than leaving it ambiguous. If a request is deliberately left without a client-side deadline (e.g. because the server may still commit the change after the client gives up), state why in a comment and ensure some other layer (a UI-level wait, a retry policy) caps the user-visible delay.

Example of guarding a custom timeout-free fetch so it doesn't break loopback routing:
```ts
export const fetchWithoutIdleTimeouts: typeof fetch = (input, init) => {
  const host = hostnameOf(input);
  const dispatcher = isLoopbackOrLocal(host)
    ? loopbackDispatcher // no timeouts, no proxy
    : envProxyDispatcher; // respects HTTP_PROXY/NO_PROXY, keeps default timeouts
  return undiciFetch(input, { ...init, dispatcher });
};
```</description>
</invoke>
