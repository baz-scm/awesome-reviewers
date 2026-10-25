---
title: API contract consistency
description: 'When designing or evolving API surfaces (HTTP headers, RPC calls, and
  event envelopes), treat them as *round-trip contracts*: don’t silently change the
  meaning of identifiers/fields, and don’t let newly introduced fields disappear across
  layers.'
repository: CLINE/cline
label: API
language: TypeScript
comments_count: 4
repository_stars: 70839
---

When designing or evolving API surfaces (HTTP headers, RPC calls, and event envelopes), treat them as *round-trip contracts*: don’t silently change the meaning of identifiers/fields, and don’t let newly introduced fields disappear across layers.

**Rules**
1) **Preserve meaning or rename the contract**
- If the *value meaning* behind a request element changes, either keep the old meaning or rename the field/header (and update consumers). Don’t reuse a name like `X-Task-ID` for a different identifier type.

2) **Guarantee field propagation across projections**
- If an event/payload field is accepted on input, it should be forwarded out consistently in every projection/copy path (e.g., server projector → hub envelope → runtime host event).
- Add tests that exercise: (a) distinct non-empty value, (b) explicitly empty value, and (c) omitted field.

3) **Make API parameters self-describing**
- Avoid boolean positional flags in public functions used across packages/modules; prefer options objects so intent is visible at call sites.

**Examples**
- HTTP header semantic drift (fix by either keeping task ID semantics or renaming):
```ts
// BAD: header name claims task id, but value is ulid
headers['X-Task-ID'] = ulid;

// GOOD: rename to match semantics
headers['X-Task-ULID'] = ulid;
// or revert to actual task id
headers['X-Task-ID'] = taskId;
```

- Event field “goes in but never comes out” (fix by forwarding):
```ts
// Server projector: include displayPrompt in the outgoing envelope
pending_prompt_submitted: ({ displayPrompt, ...rest }) => ({
  ...rest,
  displayPrompt,
});

// Runtime host conversion: carry it through to the core event
const coreEvent = {
  ...serverProjection,
  displayPrompt: serverProjection.displayPrompt,
};
```

- Boolean flags → options object:
```ts
// BAD
load(true, true); // what do the booleans mean?

// GOOD
load({ refresh: true, userInitiated: true });
```

**Test checklist (practical)**
- For every new/changed API field: verify it round-trips through all layers (request → server/projector → internal envelope → runtime host → client).
- For every identifier/header: verify backend semantics and add a compatibility note in the change log.
- For every parameter interface: ensure call sites are readable without opening the function signature.