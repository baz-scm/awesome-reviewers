---
title: API contract consistency
description: 'When extending or modifying a client/server contract (RPC operations,
  request/response payloads, HTTP headers, shared schemas), treat the whole surface
  as one piece and verify it end-to-end before merging:'
repository: "cline/cline\r\n"
label: API
language: TypeScript
comments_count: 6
repository_stars: 70946
---

When extending or modifying a client/server contract (RPC operations, request/response payloads, HTTP headers, shared schemas), treat the whole surface as one piece and verify it end-to-end before merging:

- New fields added to a request must be round-tripped back out wherever the corresponding response/event is produced. A field that goes in and never comes out is a trap for the next integrator — e.g. a `displayPrompt` accepted on input but dropped from both the server projection and the event conversion back to core.
- New operations/methods must be wired into every place that gates or dispatches the API surface (operation allow-lists, generated clients, RPC registries), not just implemented internally. An operation missing from the dispatch list is effectively unreachable even though the code exists.
- Never silently repurpose an existing field or header to carry different semantics while keeping the same name — e.g. sending a `ulid` under a header still named `X-Task-ID`. If the meaning changes, rename the field/header or add a new one so consumers aren't silently broken.
- Don't expose client methods or capabilities that the underlying protocol can't actually fulfill; if the transport has no way to perform an operation, remove the surface method rather than leaving a no-op or guessable failure.
- Avoid duplicating a piece of contract state across multiple schemas/flags (e.g. a derived "configured" boolean copied into session config). Resolve it once from the canonical/shared contract and have all consumers read from that single source instead of keeping parallel copies in sync.
- When a spec/protocol defines a MUST/MUST NOT rule (e.g. hiding tools not visible to the model), apply it unconditionally rather than gating it behind an extra flag that callers can forget to set.

Applying this checklist when touching API shapes prevents silent contract drift, unreachable operations, and duplicated state that has to be kept in sync by hand.