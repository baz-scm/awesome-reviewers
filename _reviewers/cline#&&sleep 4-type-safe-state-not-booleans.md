---
title: Type-safe state, not booleans
description: When an API parameter or interface field represents one of a small, fixed
  set of states, avoid booleans and raw strings passed by convention — model the domain
  explicitly with string-literal unions or discriminated unions so the compiler rejects
  invalid states instead of accepting them silently.
repository: cline/cline#&&sleep 4
label: API
language: TypeScript
comments_count: 4
repository_stars: 70980
---

When an API parameter or interface field represents one of a small, fixed set of states, avoid booleans and raw strings passed by convention — model the domain explicitly with string-literal unions or discriminated unions so the compiler rejects invalid states instead of accepting them silently.

Concretely:
- Don't use a boolean to encode a concept that isn't truly binary, and don't describe a state only by negating another (e.g. `promptSeeded: boolean`). Prefer a positive, named union: `seeded: "seeded" | "written"` (or similar) so each state is self-describing.
- Don't pass a free-form string as a selector/key for internal routing (e.g. a queue name like `"statusWriteQueue"`); the call site gives no indication of what's valid and the compiler can't catch typos or wrong values. Prefer passing the actual getter/setter (or dedicated small wrapper methods) instead of a string key:
  ```ts
  // Avoid:
  enqueueSessionWrite(session, "compactionStateWriteQueue", action);

  // Prefer:
  enqueueCompactionStateWrite(session, action); // internally calls chainWrite with explicit getter/setter
  ```
- When a field is only meaningful in some contexts (e.g. "only set for `beforeRun`"), encode that constraint in the type system via a discriminated union rather than a comment, so the rest of the system gets compile-time checking instead of relying on documentation:
  ```ts
  type RunLifecycleContext =
    | { phase: "beforeRun"; entry: "run" | "continue"; promptSeeded: boolean }
    | { phase: "afterRun" };
  ```
This produces fewer invalid-state bugs, removes the need for "must remember this field is only valid when X" comments, and makes call sites self-documenting and verifiable by the type checker.