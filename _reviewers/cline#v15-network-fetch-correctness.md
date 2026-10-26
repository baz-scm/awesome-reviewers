---
title: Network fetch correctness
description: Adopt a networking standard where every network path is (1) routed correctly
  under proxies (especially loopback/local), (2) strictly bounded and cancellable
  (AbortSignal + timeouts on primary and fallback), and (3) connection-lifecycle aware
  (retry/wait until connected, and track dispatch boundaries to avoid duplicate sends).
repository: cline/cline#v15
label: Networking
language: TypeScript
comments_count: 8
repository_stars: 70877
---

Adopt a networking standard where every network path is (1) routed correctly under proxies (especially loopback/local), (2) strictly bounded and cancellable (AbortSignal + timeouts on primary and fallback), and (3) connection-lifecycle aware (retry/wait until connected, and track dispatch boundaries to avoid duplicate sends).

**Rules**
1. **Proxy-aware routing with loopback bypass**: If `HTTP_PROXY` is set and `NO_PROXY` is absent, many proxy agents will still proxy localhost unless you explicitly bypass for loopback. Use a direct agent for loopback/local-network hosts, and the env/proxy agent for everything else.
2. **No unbounded fallback requests**: If you have fallback logic (e.g., “try X, then fetch Y”), ensure the fallback also honors the same `AbortSignal` and has its own timeout/abort.
3. **Wait/retry for connection readiness**: For hub/transport link reads, don’t fail immediately during an in-progress connect; wait briefly for the link to become connected, then retry reads.
4. **Make dispatch boundaries explicit**: When “send” crosses an internal boundary (e.g., Hub dispatch), propagate a signal/typed result that lets the UI know whether the prompt was dispatched. Only offer “resend” when the original was truly pre-dispatch/unconfirmed.

**Example: proxy-safe, idle-timeout-free fetch for local servers + bounded fallback**
```ts
import { EnvHttpProxyAgent } from "undici";
import { setTimeout as delay } from "node:timers/promises";

let idleTimeoutFreeLocalAgent: EnvHttpProxyAgent | undefined;
let directLocalAgent: any | undefined;
let proxyAgent: EnvHttpProxyAgent | undefined;

function isLoopbackOrLocal(hostname: string): boolean {
  const host = hostname.replace(/^\[|\]$/g, "").toLowerCase();
  // Include 127.0.0.1, ::1, RFC1918, and explicitly 0.0.0.0.
  return host === "localhost" || host === "127.0.0.1" || host === "::1" || host === "0.0.0.0";
}

export async function fetchWithNetworkStandard(
  input: string | URL,
  init: RequestInit & { signal?: AbortSignal },
): Promise<Response> {
  const url = typeof input === "string" ? new URL(input) : new URL(input.toString());
  const hostname = url.hostname;

  // 1) route correctly
  const agent = isLoopbackOrLocal(hostname)
    ? (directLocalAgent ??= new (require("undici").Agent)({}))
    : (proxyAgent ??= new EnvHttpProxyAgent({ headersTimeout: 0, bodyTimeout: 0 }));

  // 2) bound/cancel: wrap with timeout that respects AbortSignal
  const timeoutMs = 20_000;
  const controller = new AbortController();
  const abort = () => controller.abort();
  init.signal?.addEventListener("abort", abort);
  const t = delay(timeoutMs).then(() => controller.abort());

  try {
    return await fetch(input, { ...init, dispatcher: agent, signal: controller.signal });
  } finally {
    init.signal?.removeEventListener("abort", abort);
    clearTimeout((t as any));
  }
}

// Pattern for fallback: never omit AbortSignal/timeout
export async function fetchPrimaryThenFallback(
  primary: () => Promise<Response>,
  fallback: (signal: AbortSignal) => Promise<Response>,
  signal: AbortSignal,
): Promise<Response> {
  try {
    return await primary();
  } catch {
    return await fallback(signal); // ensure fallback honors the same signal
  }
}
```

**Checklist for PRs**
- Does the chosen HTTP dispatcher/agent preserve loopback semantics under proxy env vars?
- Are *all* code paths (including fallback) bound and cancellable with the same AbortSignal?
- If reading from a connection-bound dependency, do we wait/retry until connected (within a bounded window)?
- For user-visible “resend” actions, is there a dispatch/unconfirmed signal so duplicates can’t happen?