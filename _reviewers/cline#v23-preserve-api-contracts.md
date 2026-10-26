---
title: Preserve API Contracts
description: 'When changing or wiring API/SDK boundaries, ensure the contract is explicit,
  semantically correct, and preserved end-to-end—no silent meaning drift.


  Apply these rules:'
repository: cline/cline#v23
label: API
language: TypeScript
comments_count: 6
repository_stars: 70889
---

When changing or wiring API/SDK boundaries, ensure the contract is explicit, semantically correct, and preserved end-to-end—no silent meaning drift.

Apply these rules:
1) **Round-trip fields/inputs**: if the server accepts a field (e.g., `displayPrompt`), it must be carried through all projections/handlers back into the emitted client event.
2) **Keep identifiers unambiguous**: header names and their values must match. If you change what `X-Task-ID` contains, either keep the previous meaning or rename/add a new header to preserve contract clarity.
3) **Avoid ambiguous parameter shapes**: replace boolean-position parameters with an options object using named fields.
4) **Don’t silently rewrite user endpoints**: endpoint normalization must respect user-supplied URLs (avoid inheriting defaults like `/v1` when that would change meaning).
5) **Map external API fields by meaning, not by name**: when providers differ (e.g., `max_context_length` vs `loaded_context_length`), use the value that matches the behavior you need.
6) **Carry explicit scoping/identity**: for multi-step flows, resolve once and propagate an account/scope token so subsequent calls can’t silently switch accounts or require redundant re-checks.

Example (options object instead of booleans):
```ts
// Before
load(true, true)

// After
load({ refresh: true, userInitiated: true })
```