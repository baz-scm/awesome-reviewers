---
title: Explicit, honest API contracts
description: 'API parameters, options, and client methods must say exactly what they
  do, and the surface must only expose what is actually supported underneath.


  - Avoid boolean or "stringly-typed" parameters that encode ambiguous or multi-state
  behavior. A caller passing `"statusWriteQueue"` or a bare `resumed: boolean` gives
  the compiler no way to catch a wrong value...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: API
language: TypeScript
comments_count: 5
repository_stars: 70964
---

API parameters, options, and client methods must say exactly what they do, and the surface must only expose what is actually supported underneath.

- Avoid boolean or "stringly-typed" parameters that encode ambiguous or multi-state behavior. A caller passing `"statusWriteQueue"` or a bare `resumed: boolean` gives the compiler no way to catch a wrong value and forces readers to trace the implementation to know what it means. Prefer passing the actual getter/setter, a dedicated method per case, or a string union that enumerates the valid states explicitly:
  ```ts
  // Avoid:
  enqueueWrite(session, "compactionStateWriteQueue", action);

  // Prefer:
  enqueueCompactionStateWrite(session, action); // or pass {get, set} explicitly
  ```
- Don't add conditional options/flags to a client or tool surface unless the condition reflects a real behavioral difference. If the spec or protocol requires a behavior unconditionally (e.g., hiding tools not visible to the model), make it the default rather than gating it behind an option that only exists for backward compatibility — remove the option once it's safe to do so.
- Keep the client interface honest: if the underlying protocol/transport cannot support an operation (e.g., changing a running session's model when the wire protocol has no such command), remove or stub that method rather than leaving a method that silently no-ops or misleads callers about what's possible.
- Keep wire-level contracts (header names, field names) accurate to their content. If the semantic meaning of a value sent over a header or field changes (e.g., switching from task ID to ULID), rename the field or add a new one — don't silently repurpose an existing name, since that breaks any consumer relying on the documented contract.

Applying this consistently makes call sites self-documenting, lets the compiler catch misuse, and ensures the API surface never promises more than the implementation can deliver.