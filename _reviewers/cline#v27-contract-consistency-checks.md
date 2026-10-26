---
title: Contract consistency checks
description: 'Ensure API contracts are explicit and preserved end-to-end across layers
  (client → server → runtime → event projections).


  Apply these rules during code review:'
repository: cline/cline#v27
label: API
language: TypeScript
comments_count: 6
repository_stars: 70892
---

Ensure API contracts are explicit and preserved end-to-end across layers (client → server → runtime → event projections).

Apply these rules during code review:
- **Do not change field semantics without changing the API.** If the meaning of a header/body field changes, either keep the old meaning or rename the field / add a new one (or send both as separate fields).
- **All received fields must be forwarded/serialized back out.** When adding a request field (or changing an event payload), update every projection/copy path so integrators don’t hit “goes in, never comes out”.
- **Spec-driven behavior should be unconditional.** Don’t gate contract-compliance behind capability flags unless the spec explicitly allows exceptions.
- **Prefer structured, named options over booleans** for request-like APIs to prevent call-site ambiguity.
- **Avoid duplicated readiness/state flags.** Derive optional capabilities/readiness from the canonical shared contract/metadata, not from a second, host-specific UI flag.
- **Catalog parsing must accept provider variants** (field name differences) to prevent silent fallback behavior.

Example (semantic mismatch):
```ts
// Bad: header name implies one identifier, but value is a different one.
headers["X-Task-ID"] = options.ulid ?? "";

// Good: rename or add a separate header.
headers["X-Task-ID"] = options.taskId ?? "";
headers["X-Task-ULID"] = options.ulid ?? "";
```

Example (field forwarding regression):
```ts
// When you accept displayPrompt in one stage, forward it in every event copy/projection.
nextPayload.displayPrompt = input.displayPrompt;
```

Minimum checklist:
- For each added/modified field: update request DTO, validation, every event/projector copy, and add a regression test that compares payloads across both paths (server projection vs runtime handler).