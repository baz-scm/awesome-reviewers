---
title: API contract invariants
description: 'When changing or extending an API (REST headers, event payloads, tool
  listings, or renderable result formats), enforce contract invariants:


  1) **Spec-aligned behavior with no hidden exceptions**: If the spec says a host
  MUST NOT emit/list something under certain conditions, implement that rule unconditionally.
  Avoid coupling behavior to ad-hoc option flags...'
repository: cline/cline#v15
label: API
language: TypeScript
comments_count: 5
repository_stars: 70877
---

When changing or extending an API (REST headers, event payloads, tool listings, or renderable result formats), enforce contract invariants:

1) **Spec-aligned behavior with no hidden exceptions**: If the spec says a host MUST NOT emit/list something under certain conditions, implement that rule unconditionally. Avoid coupling behavior to ad-hoc option flags that mask contract drift.

2) **Meaning-preserving fields across the boundary**: If a request header name or payload field implies a specific semantic (e.g., “task id”), keep the meaning stable. If you must change the identifier, either **confirm the backend’s expected contract** and keep it, or **rename** the header / **send multiple headers** to keep semantics unambiguous.

3) **Forward new fields end-to-end**: When adding a payload field (e.g., `displayPrompt`), update *every* serialization/deserialization path and duplicate event projection so the field reliably returns to consumers.

4) **Make interface intent explicit**: Avoid boolean positional parameters in public or cross-module APIs. Use an options object so call sites are self-documenting and parameter mixups are impossible.

5) **Evolve wire/output formats as a coordinated contract**: If the producer changes output structure (e.g., tool result content shape), ensure all consumers/renderers understand the new shape; otherwise clients will display broken/escaped content.

Examples

### A) Stable header semantics
```ts
// Bad: semantic change hidden behind same header name
headers["X-Task-ID"] = ulid ?? "";

// Good: either keep the original meaning
headers["X-Task-ID"] = taskId;
// or make semantics explicit
headers["X-Task-ULID"] = ulid ?? "";
```

### B) Replace boolean parameters with options
```ts
// Bad
load(true, true); // what are the two booleans?

// Good
load({ refresh: true, userInitiated: true });
```

### C) Forward a new event field everywhere
```ts
// Ensure projections + runtime conversions both preserve displayPrompt
event.pending_prompt_submitted.displayPrompt = input.displayPrompt;
// ...and the opposite conversion path must carry it back out.
```

Adopting these invariants prevents the common failure modes shown here: spec drift, silent semantic changes, one-way payload additions, ambiguous call signatures, and consumer breakage after format changes.