---
title: API Contract Round-Trip
description: When an API contract changes (new fields, new options, new behavior gates,
  or version/identity changes), ensure it remains unambiguous and consistent across
  every boundary.
repository: cline/cline#v12
label: API
language: TypeScript
comments_count: 6
repository_stars: 70872
---

When an API contract changes (new fields, new options, new behavior gates, or version/identity changes), ensure it remains unambiguous and consistent across every boundary.

Apply this standard:
- **Avoid ambiguous parameters:** Prefer an options object over positional booleans.
  - Good: `load({ refresh: true, background: true })`
  - Bad: `load(true, true)`
- **Keep identifiers truthful:** If the header/field name implies a meaning (e.g., `X-Task-ID`), the value must match that meaning. If the meaning changes, rename (e.g., `X-Task-ULID`) or send both explicitly.
- **Round-trip new fields end-to-end:** If a request/producer introduces a new field, every projector/converter/event copy must forward it back so the consumer can see it.
  - Add a regression test that runs the payload through the real path and asserts the field is present for multiple cases (present, empty string, omitted).
- **Use the spec/authoritative contract for behavior gating:** Don’t add “compatibility” flags or duplicated readiness booleans that create synchronization work. Derive behavior from the shared provider/spec/capability source.
- **Be explicit about API versioning:** Use the correct endpoint version and normalize base URLs so version paths are built deterministically.

Example patterns:
```ts
// 1) Prefer options objects
function load(opts: { refresh?: boolean; background?: boolean } = {}) {
  const { refresh = false, background = false } = opts;
  // ...
}
load({ refresh: true });

// 2) Keep field names consistent with values
headers["X-Task-ULID"] = ulid; // if you changed meaning

// 3) Forward new fields through all copies
function projector(input: { displayPrompt?: string }) {
  return { /* ... */ displayPrompt: input.displayPrompt };
}
function runtimeHost(event: { displayPrompt?: string }) {
  return { /* ... */ displayPrompt: event.displayPrompt };
}
```

This prevents subtle “works locally but breaks integration” issues caused by mismatched contracts, lost fields, or duplicated semantics across layers.