---
title: API contract consistency
description: Treat every cross-layer interface (tool options, request/response schemas,
  headers, host methods) as a contract that must be unambiguous, symmetric, and backed
  by a single source of truth—not an implementation detail leaking through.
repository: cline/cline#zzz-unlikely-123abc
label: API
language: TypeScript
comments_count: 6
repository_stars: 71035
---

Treat every cross-layer interface (tool options, request/response schemas, headers, host methods) as a contract that must be unambiguous, symmetric, and backed by a single source of truth—not an implementation detail leaking through.

Apply this by:
- Depending on abstract capabilities, not concrete transports. A shared tool or client interface should be defined against a contract (e.g. a storage/session interface) that both local and cloud implementations satisfy, rather than hard-wiring it to one backend's auth/session requirements.
- Collapsing redundant flags/fields into one authoritative switch. If a capability is already gated by one option (e.g. a client factory flag) or governed by a spec rule, don't add a second flag that can disagree with it; conformance should be unconditional where the spec requires it.
- Not exposing operations the underlying protocol can't actually perform. If a method (e.g. `updateSessionModel`) has no backing capability in the transport/protocol, remove it from the interface rather than leaving a silent no-op or throwing surprise.
- Keeping fields symmetric end-to-end. Any field accepted on input (e.g. `displayPrompt`) must be forwarded through every corresponding output/event path; a field that goes in but never comes out is a trap for future integrators.
- Naming headers/fields for what they actually carry. If a header's semantics change (e.g. `X-Task-ID` now carries a `ulid` instead of a task id), rename it or keep both values distinct rather than silently repurposing an established contract.
- Avoiding duplicated state across layers. Derive optional/computed properties (e.g. `providerConfigured`) from the single shared contract (e.g. provider metadata) instead of introducing a parallel flag that must be kept in sync by hand.

Example: instead of
```ts
"X-Task-ID": this.options.ulid || "",
```
either keep the header's original meaning or rename it:
```ts
"X-Task-ULID": this.options.ulid || "",
```
so the contract stays unambiguous for consumers on both ends.