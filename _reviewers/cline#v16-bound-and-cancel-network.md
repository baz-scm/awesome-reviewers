---
title: Bound and Cancel Network
description: Network code must have explicit, consistent timeout and cancellation
  behavior on *every* path (primary, fallback, retries), and must select the correct
  HTTP/transport strategy for the target (local streaming vs remote/proxied).
repository: cline/cline#v16
label: Networking
language: TypeScript
comments_count: 6
repository_stars: 70882
---

Network code must have explicit, consistent timeout and cancellation behavior on *every* path (primary, fallback, retries), and must select the correct HTTP/transport strategy for the target (local streaming vs remote/proxied).

Apply:
1) Bound/cancel all fetches
- Every network call (including fallbacks) must use an AbortSignal or an explicit timeout.
- Never rely on “the primary call is bounded” if a fallback can hang.

2) Choose the right HTTP agent per scenario
- If local servers stream slowly, disable/adjust idle timeouts only for those scenarios.
- Preserve loopback/direct routing when HTTP proxy env vars are set; add regression tests with HTTP_PROXY set and NO_PROXY unset.
- Gate local-network behavior with robust address detection (handle 0.0.0.0 and mapped loopback).

3) Document and preserve intentional deadline tradeoffs
- If you remove/relax client deadlines to let the server commit after the UI gives up, document the behavior and ensure UI waits are still bounded by the appropriate user-facing timer.

Example (pattern: bounded fetch with AbortSignal, including fallback):
```ts
async function fetchWithTimeout(url: string, ms: number, signal?: AbortSignal) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(new Error('timeout')), ms);

  // Forward cancellation
  if (signal) {
    if (signal.aborted) controller.abort(signal.reason);
    signal.addEventListener('abort', () => controller.abort(signal.reason), { once: true });
  }

  try {
    return await fetch(url, { signal: controller.signal });
  } finally {
    clearTimeout(timeout);
  }
}

async function fetchModelIds() {
  try {
    return await fetchWithTimeout('/api/v1/models', 5000);
  } catch {
    // Fallback must also be bounded/cancellable
    return await fetchWithTimeout('/api/v1/models/source', 5000);
  }
}
```