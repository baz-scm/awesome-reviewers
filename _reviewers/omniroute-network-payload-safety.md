---
title: Network payload safety
description: 'When implementing HTTP/SSE adapters or transforming network responses/streams,
  enforce three rules: (1) preserve required response headers/trace metadata while
  normalizing body-related headers, (2) respect protocol framing so streamed events
  can’t merge, and (3) prevent hanging outbound calls with timeouts.'
repository: diegosouzapw/OmniRoute
label: Networking
language: TypeScript
comments_count: 3
repository_stars: 33162
---

When implementing HTTP/SSE adapters or transforming network responses/streams, enforce three rules: (1) preserve required response headers/trace metadata while normalizing body-related headers, (2) respect protocol framing so streamed events can’t merge, and (3) prevent hanging outbound calls with timeouts.

Apply this as a checklist:
- **After filtering/rewriting an HTTP response:** reuse upstream headers that clients depend on (e.g., request/trace/version), but set/reset **Content-Type** appropriately and avoid stale **Content-Length**.
- **For SSE/streaming transforms:** ensure every enqueued “event” ends with a proper SSE delimiter (`\n\n`) so later sentinel/stop messages don’t concatenate with buffered tail data.
- **For outbound network calls:** wrap `fetch` (or equivalent) with an `AbortController` timeout; treat timeouts as recoverable failures where possible.

Example patterns:

```ts
// 1) HTTP response transformation: preserve trace/version headers
function buildTransformedResponse(upstream: Response, data: any) {
  const newHeaders = new Headers(upstream.headers);
  // normalize payload headers for the transformed body
  newHeaders.set("Content-Type", "application/json");
  newHeaders.delete("Content-Length");
  return new Response(JSON.stringify(data), {
    status: upstream.status,
    headers: newHeaders,
  });
}

// 2) SSE framing: always end events with a delimiter
function enqueueSseEvent(controller: TransformStreamDefaultController, prefix: string, payload: string) {
  controller.enqueue(new TextEncoder().encode(`${prefix}${payload}\n\n`));
}

// 3) Outbound request timeout
async function fetchWithTimeout(url: string, init: RequestInit = {}, timeoutMs = 7000) {
  const ac = new AbortController();
  const t = setTimeout(() => ac.abort(), timeoutMs);
  try {
    return await fetch(url, { ...init, signal: ac.signal });
  } finally {
    clearTimeout(t);
  }
}
```

Teams should require these checks in code review for any networking code that adapts/streams/transforms data.