---
title: API contract drift prevention
description: 'Treat every boundary across services/adapters/providers as a stable
  contract: request/response fields must be forwarded end-to-end, operation names
  must remain reachable, and any provider-specific shape/version rules must be explicit
  and tested.'
repository: cline/cline#v21
label: API
language: TypeScript
comments_count: 6
repository_stars: 70886
---

Treat every boundary across services/adapters/providers as a stable contract: request/response fields must be forwarded end-to-end, operation names must remain reachable, and any provider-specific shape/version rules must be explicit and tested.

Apply this checklist:
- **Forward all contract fields end-to-end:** if a field is accepted by an upstream envelope, ensure *every* projection/event-copy path preserves it.
- **Keep identifiers semantically unambiguous:** if a header/name changes meaning (e.g., task id → ulid), rename the header or send both identifiers in separate fields—don’t rely on backend inference.
- **Conform to capability/visibility rules unconditionally:** hosts should not list resources/tools that the consumer can never call per spec; avoid “it’s fine when apps are off” exceptions.
- **Version and normalize paths explicitly:** when endpoints vary by version (e.g., `/v0` vs `/v1`), normalize input base URLs (trailing slashes, optional prefixes) before constructing the final path.
- **Pin provider adapter request shapes with wire/contract tests:** add tests that assert the exact provider request fields required for the adapter floor (e.g., `reasoning.effort` vs legacy fields).

Example rule of thumb for the “field goes in but doesn’t come out” case:
```ts
// Bad: accept displayPrompt but drop it in one projection/copy.
// Good: preserve it in *all* event copies/handlers.
function projector(inEvent: { displayPrompt?: string }) {
  return {
    ...inEvent,
    displayPrompt: inEvent.displayPrompt,
  };
}

function runtimeHandler(envelope: { displayPrompt?: string }) {
  const coreEvent = {
    // must include displayPrompt
    displayPrompt: envelope.displayPrompt,
    // ...other fields
  };
  return coreEvent;
}
```