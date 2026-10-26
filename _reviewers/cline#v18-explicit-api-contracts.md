---
title: Explicit API Contracts
description: 'Ensure public/API-facing behavior is contract-correct, self-describing,
  and end-to-end consistent.


  Apply these rules:

  1) Enforce spec invariants unconditionally'
repository: cline/cline#v18
label: API
language: TypeScript
comments_count: 4
repository_stars: 70884
---

Ensure public/API-facing behavior is contract-correct, self-describing, and end-to-end consistent.

Apply these rules:
1) Enforce spec invariants unconditionally
- If the protocol spec defines required filtering/visibility, implement it regardless of optional feature flags.

2) Make function parameters self-describing
- Avoid boolean positional flags for behavior control. Prefer an options object with named fields.

3) Guarantee request/response field round-tripping
- If a request field is accepted, every projection/conversion layer that copies the payload must forward it back out.

4) Never silently change semantics under an existing contract name
- For headers/fields, keep the name aligned with the value’s meaning. If you must change what the value represents, rename the header (or add a new one) rather than repurposing the old.

Example (boolean -> options object):
```ts
// Bad
load(true, true); // what do these booleans mean?

// Good
load({ refresh: true, background: true });
```

Example (round-trip forwarding):
```ts
// When mapping events, carry fields through both copies
const forwarded = {
  ...source,
  displayPrompt: source.displayPrompt,
};
```

Example (contract-safe header evolution):
```ts
// If X-Task-ID must remain a task identifier:
headers["X-Task-ID"] = taskId;
headers["X-Task-ULID"] = ulid;
```