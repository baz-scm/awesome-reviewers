---
title: Preserve API Contracts
description: 'When changing API-adjacent behavior, treat the contract as “semantic
  + shape + invariants,” and ensure every boundary keeps it intact.


  Checklist:

  - **Spec invariants are unconditional:** If the protocol says the host MUST NOT
  include certain items unless a condition is met, don’t add feature-flag exceptions.'
repository: cline/cline#v17
label: API
language: TypeScript
comments_count: 5
repository_stars: 70883
---

When changing API-adjacent behavior, treat the contract as “semantic + shape + invariants,” and ensure every boundary keeps it intact.

Checklist:
- **Spec invariants are unconditional:** If the protocol says the host MUST NOT include certain items unless a condition is met, don’t add feature-flag exceptions.
- **Header meaning must match the header name:** If you change what a header carries, either keep the original meaning or rename/add a new header so the backend contract stays unambiguous.
- **Forward new fields through every projection/copy:** If a field is added to an input/event, ensure it’s propagated through all intermediate event copies and mappings.
- **Keep provider-specific shapes/fields:** Preserve catalog fields and map known provider aliases (e.g., different limit field names) rather than falling back to defaults.
- **Prefer options objects over boolean parameters** for any public/used-by-others function that represents API request modes (e.g., refresh vs background).

Example: header contract safety
```ts
// Bad: header name says task id, value now carries ulid
headers["X-Task-ID"] = options.ulid ?? "";

// Good (pick one):
// 1) Keep original meaning
headers["X-Task-ID"] = options.taskId ?? "";

// 2) Or rename/add a new header
headers["X-Task-ULID"] = options.ulid ?? "";
```

Example: forward added event fields
```ts
// Ensure every projection/copy includes the new field.
nextEvent.displayPrompt = input.displayPrompt;
```

Example: unambiguous interface inputs
```ts
// Bad
load(true, true); // what do these mean?

// Good
load({ refresh: true, background: true });
```