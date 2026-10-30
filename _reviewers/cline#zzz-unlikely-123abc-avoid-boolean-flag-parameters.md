---
title: Avoid boolean flag parameters
description: 'Functions that take one or more unnamed boolean arguments are hard to
  read and easy to misuse at the call site: `load(true, true)` or `enqueueSessionWrite(session,
  "compactionStateWriteQueue", action)` give no indication of what each value means,
  and the compiler won''t catch a swapped or wrong value. The same problem shows up
  with ad-hoc string keys used to...'
repository: cline/cline#zzz-unlikely-123abc
label: Code Style
language: TypeScript
comments_count: 3
repository_stars: 71035
---

Functions that take one or more unnamed boolean arguments are hard to read and easy to misuse at the call site: `load(true, true)` or `enqueueSessionWrite(session, "compactionStateWriteQueue", action)` give no indication of what each value means, and the compiler won't catch a swapped or wrong value. The same problem shows up with ad-hoc string keys used to select a field/behavior — they look type-safe but accept any string and convey no intent.

Prefer one of these alternatives:
- An options object with named, defaulted properties, so call sites are self-documenting:
  ```ts
  function load({ refresh = false, userInitiated = false } = {}) { ... }
  // call site
  load({ refresh: true, userInitiated: true })
  ```
- A discriminated/string union when the flag represents a mode or state with more than two meaningful values, or when future states are likely (e.g. `resumeKind: "agent_start" | "agent_resume"` instead of `resumed?: boolean`).
- Explicit getter/setter pairs or dedicated small wrapper methods instead of a shared helper keyed by a field-name string, so the type system — not a string literal — determines behavior (e.g. `enqueueStatusWrite`/`enqueueCompactionStateWrite` each passing their own accessor pair into one shared `chainWrite`, rather than passing `"statusWriteQueue"`).

Apply this whenever a function signature grows a second or third boolean/string parameter, or whenever reviewing new APIs: ask whether the parameter's meaning is obvious from the call site alone. If not, convert it to a named options object or a union type before merging.