---
title: API Contract Clarity
description: 'When changing or adding API surface, treat the wire/contract as fixed:
  preserve meaning, ensure fields propagate end-to-end, and avoid ambiguous interface
  parameters.'
repository: cline/cline#v8
label: API
language: TypeScript
comments_count: 5
repository_stars: 70867
---

When changing or adding API surface, treat the wire/contract as fixed: preserve meaning, ensure fields propagate end-to-end, and avoid ambiguous interface parameters.

Apply these checks:
1) **Spec-mandated behavior is unconditional**: if the spec says the host MUST NOT list tools not visible to the model, don’t gate it behind capability/option flags.
2) **End-to-end field propagation**: any input field you accept on the API boundary must be forwarded through all event/request copies and emitted back consistently.
3) **Unambiguous identifiers**: don’t change the *meaning* of a header/request field without either renaming it (e.g. `X-Task-ULID`) or adding a parallel header so backend logic can’t silently misattribute.
4) **No boolean positional parameters at boundaries**: replace `load(true, false)`-style calls with named options.
5) **Single source of truth**: don’t duplicate “readiness/configured” flags across client/session layers—derive them from the shared provider contract/metadata so the interface can’t drift.

Example (prefer options object over booleans):
```ts
// Prefer
load({ refresh: true, background: true });

// Instead of
load(true, true);
```