---
title: API contract integrity
description: 'Design interfaces, request/response shapes, and event payloads as explicit,
  stable contracts rather than incidental artifacts of one implementation:


  - **Decouple contracts from implementations.** A shared tool/interface used by multiple
  backends (e.g. local vs. cloud) should depend on an abstract contract (storage,
  session, etc.) that each backend...'
repository: cline/cline#"><b>zze3729958
label: API
language: TypeScript
comments_count: 9
repository_stars: 71067
---

Design interfaces, request/response shapes, and event payloads as explicit, stable contracts rather than incidental artifacts of one implementation:

- **Decouple contracts from implementations.** A shared tool/interface used by multiple backends (e.g. local vs. cloud) should depend on an abstract contract (storage, session, etc.) that each backend implements, not on one backend's specific transport or session model. If a feature only works for one implementation, extract the contract and exercise it against all implementations.
- **Keep field/header semantics stable.** If a header or field's documented meaning is `taskId`, don't silently repurpose it to carry a different value (e.g. a `ulid`) — rename the field/header or add a new one so the wire contract stays unambiguous to consumers.
- **Preserve round-trip symmetry.** Any field accepted on input (e.g. `displayPrompt`) must be propagated through every corresponding output/event path. A field that goes in and never comes back out is a trap for the next integrator — audit all projection/serialization sites when adding a field.
- **Avoid boolean or bare-string parameters for multi-state concepts.** A lone boolean (e.g. `resumed`) or a string used to select behavior (e.g. passing a queue's field name as a string) hides invalid states and gives callers no compile-time safety. Prefer a string union that models the real states, or pass explicit getter/setter pairs / dedicated methods instead of a generic string-keyed one.
- **Keep the public surface minimal and truthful to capabilities.** Don't ship an option/flag whose behavior should always be on (e.g. a visibility filter required by spec), and remove methods that the underlying protocol can't actually support (e.g. `updateSessionModel` when the hub has no such command) rather than leaving a method that silently no-ops or misleads callers.
- **Give client-facing identifiers (ids, revisions) a well-defined lifetime** so actions referencing them (skip/use/refresh) behave predictably across state updates; don't let an id's meaning shift mid-interaction.

Example of the string-flag anti-pattern to avoid:
```ts
// Bad: caller passes a field name as a string, compiler won't catch typos
this.enqueueSessionWrite(session, "compactionStateWriteQueue", action);

// Good: dedicated method with explicit getter/setter, or its own method
enqueueCompactionStateWrite(session, action) {
  return this.chainWrite(session, () => session.compactionStateWriteQueue,
    (q) => { session.compactionStateWriteQueue = q; }, action);
}
```
Apply this standard whenever adding or changing endpoints, event payloads, headers, or public interface options.