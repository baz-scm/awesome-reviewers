---
title: Explicit API Contracts
description: 'Treat every boundary-crossing value (headers, request/response fields,
  and multi-step RPC identities) as a public API contract: keep meaning unambiguous,
  preserve fields across projections, and carry explicit scope/state.'
repository: cline/cline#v16
label: API
language: TypeScript
comments_count: 6
repository_stars: 70882
---

Treat every boundary-crossing value (headers, request/response fields, and multi-step RPC identities) as a public API contract: keep meaning unambiguous, preserve fields across projections, and carry explicit scope/state.

Rules:
1) Avoid booleans in API-facing options/state. Use named options or a string union/state model so call sites can’t silently swap meaning.
2) Ensure fields round-trip. If a field is accepted in one layer/event projection, it must be forwarded consistently through every copy/handler.
3) Keep header/value semantics aligned. If you change what `X-Task-ID` contains, either keep the contract (send the original identifier) or rename the header (or add a new header) so backend attribution/rate-limiting doesn’t change silently.
4) Carry explicit scope/identity tokens in multi-step flows. Don’t rely on repeated “account hasn’t changed” checks alone; include the scope/owner token in intermediate snapshots so subsequent calls can’t cross accounts/providers.
5) Normalize versioned URLs consistently before appending endpoints (e.g., strip optional `/v1`, handle trailing slashes) so clients and servers compose the same final path.

Example (options object + header contract alignment + field forwarding pattern):
```ts
// 1) Replace booleans with an options object
function load(args: { refresh?: boolean; userInitiated?: boolean } = {}) {
  const { refresh = false, userInitiated = false } = args;
  // ...
}

// 2) Keep header name/value semantics aligned
// Either keep sending the task identifier:
headers["X-Task-ID"] = taskId;
// Or rename if sending ULID:
headers["X-Task-ULID"] = ulid;

// 3) Round-trip a field through projections
function toHubEnvelope(coreEvent: { displayPrompt?: string }) {
  return { displayPrompt: coreEvent.displayPrompt /* ... */ };
}
function fromHubEnvelope(envelope: { displayPrompt?: string }) {
  return { displayPrompt: envelope.displayPrompt /* ... */ };
}
```