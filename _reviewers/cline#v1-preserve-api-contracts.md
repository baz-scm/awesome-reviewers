---
title: Preserve API Contracts
description: Implement and enforce API/spec invariants at the boundary so observable
  behavior stays stable across transformations (request→backend, backend→events/projections,
  client↔host).
repository: cline/cline#v1
label: API
language: TypeScript
comments_count: 5
repository_stars: 70862
---

Implement and enforce API/spec invariants at the boundary so observable behavior stays stable across transformations (request→backend, backend→events/projections, client↔host).

Guidelines:
1) No semantic drift in names/identifiers: if a header/field name implies a meaning (e.g., `X-Task-ID`), keep the value aligned with that meaning; if you must change content, rename or add a new header/field.
2) Forward new fields end-to-end: when you accept a field in an input type, ensure every server-side projection and event conversion path carries it back out (avoid “field goes in, never comes out”).
3) Enforce spec rules unconditionally: if the spec says a condition always applies (e.g., tool visibility not including `"model"` must not be listed), don’t gate it behind unrelated feature flags—only keep gating where it truly belongs.
4) Encode invariants in schemas: add explicit constraints (e.g., non-empty arrays) so invalid inputs fail with the intended, stable error (not incidental type/union errors).
5) Avoid duplicated readiness/config flags: prefer deriving readiness from the shared contract rather than keeping parallel booleans that can drift.

Example (schema boundary invariant with Zod):
```ts
import { z } from "zod";

const RunCommandsInput = z.array(z.string().min(1)).min(1); // empty => clear “min items” error

export function normalizeRunCommandsInput(input: unknown): string[] {
  return RunCommandsInput.parse(input);
}
```

Practical checklist before merging API changes:
- Do request headers/fields keep the same meaning as their names?
- Does every transformation layer (projection/event mapping/client adapters) forward the new/changed field(s)?
- Are spec-required filters/visibility gates applied as the spec states?
- Are input invariants enforced in the schema (not just in downstream logic)?
- Is there any duplicated readiness/config state that should be derived from the shared contract instead?