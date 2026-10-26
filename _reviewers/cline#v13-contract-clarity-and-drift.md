---
title: Contract clarity and drift
description: Any boundary that acts like an API contract (spec rules, cross-service
  headers, shared metadata/state, and structured payload shapes) must be unambiguous,
  spec-compliant, and kept in sync across producers and consumers.
repository: cline/cline#v13
label: API
language: TypeScript
comments_count: 5
repository_stars: 70874
---

Any boundary that acts like an API contract (spec rules, cross-service headers, shared metadata/state, and structured payload shapes) must be unambiguous, spec-compliant, and kept in sync across producers and consumers.

Apply these rules:
1) **Enforce the published contract everywhere**
   - No “fallback” behavior that contradicts the spec (e.g., visibility rules must not become conditional on unrelated feature flags).
2) **Make field meaning match its name**
   - If you change what an identifier represents, either keep the old meaning or rename/add a new field/header so the contract doesn’t silently change.
   - Example (header contract):
     ```ts
     // Bad: name suggests task id, value is now ulid
     headers["X-Task-ID"] = ulid;

     // Better: keep name+meaning or introduce an explicit new contract
     headers["X-Task-ID"] = taskId;
     headers["X-Task-ULID"] = ulid;
     ```
3) **Avoid duplicating “source-of-truth” state across layers**
   - If readiness/config comes from a shared provider contract/catalog, read it from that contract rather than re-computing/storing parallel booleans in a local schema.
4) **Use explicit, named parameters for internal “API-like” functions**
   - Avoid boolean parameters whose meaning is unclear at call sites; prefer options objects.
   - Example:
     ```ts
     // Bad: unclear boolean parameters
     load(true, true);

     // Better
     load({ refresh: true, background: true });
     ```
5) **Schema evolution requires synchronized updates**
   - When you change the shape/structure of structured results (e.g., tool result content blocks), update all downstream consumers (renderers, extractors, serializers) in the same change so they don’t fall back to incorrect formatting.

This standard prevents silent behavior changes, UI regressions, and hard-to-debug cross-layer inconsistencies—especially when flags, identifiers, or payload shapes evolve over time.