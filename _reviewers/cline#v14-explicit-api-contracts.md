---
title: Explicit API Contracts
description: 'When designing or evolving API surfaces (including internal RPC/events),
  ensure the contract is unambiguous, stable, and faithfully transported.


  Apply these rules:'
repository: cline/cline#v14
label: API
language: TypeScript
comments_count: 5
repository_stars: 70876
---

When designing or evolving API surfaces (including internal RPC/events), ensure the contract is unambiguous, stable, and faithfully transported.

Apply these rules:
- **Preserve semantic meaning or rename:** If a request header/field changes meaning, either keep the old meaning or rename to reflect the new content (avoid “same name, different semantics”).
  - Example (bad): `"X-Task-ID": ulid`.
  - Fix: keep sending the task id, or rename to `X-Task-ULID`, or send both as separate headers.
- **No “field goes in, never comes out”:** Any added request/input field must be forwarded through all intermediate layers/copies so clients and downstream consumers can rely on it.
- **Prefer explicit structures over boolean flags:** Use an options object or enums for parameters where call sites otherwise can’t tell meaning (or where a boolean represents a domain state).
  - Instead of `load(refresh, background)` use `load({ refresh: true, background: true })`.
  - Instead of `entry?: boolean` use `entry?: "run" | "continue"` (or another domain enum).
- **Enforce spec rules consistently:** Don’t weaken/branch spec compliance based on unrelated feature flags/capabilities unless the spec explicitly allows it. If the protocol says a host “MUST NOT” do something, implement it unconditionally.

This reduces silent incompatibilities across clients, services, and event pipelines, and makes changes easier to review and integrate safely.