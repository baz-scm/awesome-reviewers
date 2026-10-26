---
title: Preserve API Contracts
description: 'When building or evolving cross-layer APIs (Hub/RPC, HTTP handlers,
  event/projector pipelines, and spec-driven interfaces), treat the contract as immutable:
  wire it correctly, propagate fields end-to-end, and never silently change identifier
  meaning.'
repository: cline/cline#v26
label: API
language: TypeScript
comments_count: 4
repository_stars: 70893
---

When building or evolving cross-layer APIs (Hub/RPC, HTTP handlers, event/projector pipelines, and spec-driven interfaces), treat the contract as immutable: wire it correctly, propagate fields end-to-end, and never silently change identifier meaning.

Apply this checklist:
- **Operation wiring:** If a client calls an RPC/Hub operation, ensure it’s registered/exposed on the server side (and covered by tests).
- **End-to-end field propagation:** Any request/input field added to one stage must be forwarded through *all* corresponding server projections and back out in responses/events.
- **Spec-driven gating is unconditional:** If the spec says a host must not list tools whose `visibility` doesn’t include `"model"`, don’t add exceptions based on unrelated feature flags.
- **Semantic stability:** Don’t reuse an existing field/header name if its *meaning* changes. Either keep the old meaning, or version/rename clearly (e.g., add `X-Task-ULID` instead of overloading `X-Task-ID`).
- **Explicit scope binding:** If account/scope can change mid-flow, carry an explicit scope token in the API-visible snapshot/state so later operations can’t silently target a different account.

Example anti-pattern to avoid (semantic change):
```ts
// Bad: header name unchanged, meaning changed silently
headers["X-Task-ID"] = ulid;
```

Example preferable approach:
```ts
headers["X-Task-ID"] = taskId;       // preserve meaning
headers["X-Task-ULID"] = ulid;     // add new contract field
```