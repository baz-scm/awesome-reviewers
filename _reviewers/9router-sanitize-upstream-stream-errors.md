---
title: Sanitize Upstream Stream Errors
description: 'When handling upstream streaming responses (SSE/streaming APIs), treat
  any non-stream payload (e.g., HTML error pages) as untrusted input: do not pipe
  it through streaming transforms, and do not reflect raw upstream text/HTML into
  client errors.'
repository: decolua/9router
label: Security
language: JavaScript
comments_count: 1
repository_stars: 23951
---

When handling upstream streaming responses (SSE/streaming APIs), treat any non-stream payload (e.g., HTML error pages) as untrusted input: do not pipe it through streaming transforms, and do not reflect raw upstream text/HTML into client errors.

Actionable standard:
- Validate `Content-Type` before piping/transforming.
- If it’s not the expected streaming type, consume the body and produce a *safe* error message:
  - extract a small, human-readable string (e.g., from `<title>`),
  - strip tags/avoid raw HTML,
  - clamp length before including it in any client-visible response,
  - return a clean JSON error payload.
- Ensure the error path is handled consistently (e.g., call stream error handlers / avoid router-crash scenarios).

Example pattern:
```js
const upstreamContentType = (providerResponse.headers.get('content-type') || '').toLowerCase();
if (
  upstreamContentType &&
  !upstreamContentType.includes('text/event-stream') &&
  !upstreamContentType.includes('application/json')
) {
  const bodyText = await providerResponse.text().catch(() => '');
  const titleMatch = bodyText.match(/<title>([^<]+)<\/title>/i);

  // Sanitized + clamped message (never reflect raw upstream HTML)
  const shortMsg =
    titleMatch?.[1]?.trim() ||
    (bodyText.length < 200 ? bodyText.trim() : `Upstream returned ${upstreamContentType}`);
  const safeMsg = shortMsg.replace(/<[^>]*>/g, '').slice(0, 160);

  return json({ error: safeMsg }, { status: providerResponse.status || 502 });
}
```