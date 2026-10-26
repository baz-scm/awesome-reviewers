---
title: Connection-aware Networking
description: Network code should be resilient to transient connection states, and
  never rely on implicit timeouts—while still preserving correct proxy/loopback routing.
repository: cline/cline#v24
label: Networking
language: TypeScript
comments_count: 5
repository_stars: 70891
---

Network code should be resilient to transient connection states, and never rely on implicit timeouts—while still preserving correct proxy/loopback routing.

Apply these rules:
1) Make reads/writes connection-state aware
- If a dependency is “connecting,” wait briefly for a connected state before failing.
- If the link drops and reconnects, retry at least once after reconnection.
- If the dependency is disposed/no hub is running, fail fast.

2) Propagate AbortSignal (and/or hard timeouts) to every fetch path
- Ensure fallbacks and secondary calls also use the same AbortSignal/timeout; avoid any unbounded `fetch` after a bounded primary call fails.

Example pattern (bounded + abortable fallback):
```ts
async function fetchWithAbortFallback(primary: () => Promise<any>, fallback: (signal: AbortSignal) => Promise<any>) {
  const ac = new AbortController();
  const t = setTimeout(() => ac.abort(new Error("timeout")), 5000);
  try {
    return await primary();
  } catch {
    return await fallback(ac.signal); // fallback MUST also honor signal
  } finally {
    clearTimeout(t);
  }
}
```

3) Preserve loopback/direct routing under proxy env vars
- If you introduce a custom undici/dispatcher to change timeouts, ensure it still follows the project’s “always direct to loopback” behavior.
- Add regression tests with `HTTP_PROXY` set and `NO_PROXY` unset to verify `127.0.0.1`/`localhost` behavior.

4) Correctly detect “local network” edge cases
- If you route requests differently for local model servers, ensure your local-network detection includes common variants like `0.0.0.0` and IPv4-mapped loopback.
- Add tests for these address forms to prevent silent fallback to the wrong fetch strategy.

These changes prevent: (a) empty/failed reads during connect (use readiness+retry), (b) hangs from unbounded fallbacks (use AbortSignal everywhere), and (c) broken localhost setups when proxies are present (preserve loopback and test it).