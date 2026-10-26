---
title: Explicit API Contracts
description: 'When code crosses an API boundary (client↔server, host↔backend, runtime↔events,
  or model gateway↔provider), make the contract unambiguous and stable: (1) preserve
  field/header semantics end-to-end, (2) propagate every supported field through all
  projections/copies, (3) use explicit named options instead of boolean positional
  parameters, and (4) treat...'
repository: cline/cline#v9
label: API
language: TypeScript
comments_count: 4
repository_stars: 70868
---

When code crosses an API boundary (client↔server, host↔backend, runtime↔events, or model gateway↔provider), make the contract unambiguous and stable: (1) preserve field/header semantics end-to-end, (2) propagate every supported field through all projections/copies, (3) use explicit named options instead of boolean positional parameters, and (4) treat endpoint version/URL composition as part of the contract and test common variants.

How to apply
- Payload/event propagation: if an input field exists (e.g., `displayPrompt`), ensure *every* event copy/projector/handler round-trips it.
- Header semantics: never change what a header value *means* without either (a) keeping the original identifier, or (b) renaming the header (and documenting the new meaning) or sending both identifiers.
- Options objects: replace `load(true, true)`-style APIs with named options so call sites are self-describing.
- Versioned URLs: explicitly build versioned endpoints and normalize input base URLs (trailing slashes, optional `/v1` prefixes); add tests for each variant.

Example: options object instead of booleans
```ts
// Before (ambiguous)
load(refresh, background);

// After (self-describing)
load({ refresh: true, background: false });

function load(opts: { refresh?: boolean; background?: boolean } = {}) {
  const { refresh = false, background = false } = opts;
  // ...
}
```

Example: preserve a payload field across copies
```ts
// Ensure all event projections include the field
const event = {
  sessionId: input.sessionId,
  input: input.prompt,
  displayPrompt: input.displayPrompt,
};
// ...and every downstream mapping forwards it back out.
```

Example: header value meaning must be explicit
```ts
// If backend expects task id, don't silently send ulid under the same header.
headers["X-Task-ID"] = options.taskId ?? "";
// OR rename to match semantics:
headers["X-Task-ULID"] = options.ulid ?? "";
```