---
title: Avoid ambiguous boolean/string parameters
description: Function signatures using positional booleans, or strings that stand
  in for booleans, make call sites unreadable and let the compiler accept a wrong
  value silently. A reader cannot tell what `load(true, true)` or `enqueueWrite(session,
  "statusWriteQueue", action)` means without chasing the definition, and swapping
  two booleans or mistyping a field name...
repository: cline/cline#1
label: Code Style
language: TypeScript
comments_count: 3
repository_stars: 71024
---

Function signatures using positional booleans, or strings that stand in for booleans, make call sites unreadable and let the compiler accept a wrong value silently. A reader cannot tell what `load(true, true)` or `enqueueWrite(session, "statusWriteQueue", action)` means without chasing the definition, and swapping two booleans or mistyping a field name produces no type error.

Prefer one of these, depending on the shape of the state:
- For call-site clarity with multiple flags, use a named options object with destructured defaults instead of positional booleans:
  ```ts
  // Bad
  load(true, true)

  // Good
  function load({ refresh = false, userInitiated = false } = {}) { ... }
  load({ refresh: true, userInitiated: true })
  ```
- For state that can take on more than two meaningful values, or that may grow, use a string union instead of a boolean so invalid combinations are unrepresentable and callers self-document intent (e.g. a `resumed?: boolean` flag is better expressed as part of a `runMode: "start" | "resume"`-style union when more states are plausible).
- When a parameter is really "pick which object field to operate on," don't pass the field name as a string. Pass the getter/setter pair (or a small per-field wrapper method) so the compiler enforces correctness instead of accepting any string:
  ```ts
  // Bad
  enqueueWrite(session, "compactionStateWriteQueue", action)

  // Good
  enqueueCompactionStateWrite(session, action) // internally shares one chainWrite(getter, setter, action)
  ```

Apply this whenever a new parameter is "on/off" or "mode A vs mode B" and the call site would otherwise read as an unlabeled literal.