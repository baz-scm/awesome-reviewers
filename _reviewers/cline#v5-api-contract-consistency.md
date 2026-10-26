---
title: API Contract Consistency
description: When you change or add an API field (including internal RPC/projections
  and UI-facing payload shapes), preserve both **round-trip behavior** (request →
  server/projection → response/event → renderer) and **semantic meaning** (field names
  match values and documented behavior). Also, make API-style helper functions hard
  to misuse.
repository: cline/cline#v5
label: API
language: TypeScript
comments_count: 6
repository_stars: 70864
---

When you change or add an API field (including internal RPC/projections and UI-facing payload shapes), preserve both **round-trip behavior** (request → server/projection → response/event → renderer) and **semantic meaning** (field names match values and documented behavior). Also, make API-style helper functions hard to misuse.

Rules:
1. **Round-trip new fields end-to-end**: if the backend/event envelope accepts a field, ensure every projection/copy path forwards it back out. Add regression coverage that exercises omitted vs empty vs non-empty values.
2. **Don’t silently change semantics without changing the contract**: if an identifier’s meaning changes (e.g., task id → ulid), either keep sending the originally expected identifier or rename/add headers/fields so the backend contract remains unambiguous.
3. **Interpret provider API fields semantically, not structurally**: when different providers reuse similar-looking fields (e.g., context_length vs loaded_context_length), prefer the field that matches runtime behavior to avoid wrong limits.
4. **Carry explicit scope in stateful flows**: for multi-account or multi-tenant operations, include a scope token in the snapshot/state and validate it on subsequent calls to prevent silent account switching.
5. **Prefer named options objects over boolean flags** in API-like functions/helpers (especially where behavior changes affect requests/responses).

Example (options object instead of booleans):
```ts
// Before (hard to mix up):
load(true, true);

// After (self-documenting):
load({ refresh: true, background: true });
```

Example (round-trip forwarding test target):
- If your server accepts `displayPrompt`, ensure both (a) the projector that creates the pending prompt event and (b) the runtime-host conversion back into a Core event include `displayPrompt`, then test: present/non-empty, empty string, and omitted.

Applying this standard prevents “field accepted but never returned,” “header/value meaning drift,” and “renderer/projection shape mismatch” bugs that only surface later in integrations.