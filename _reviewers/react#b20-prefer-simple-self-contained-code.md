---
title: Prefer simple, self-contained code
description: Favor the simplest construct that accomplishes the goal, and avoid unnecessary
  indirection, helper abstractions, or parameters when the same result can be expressed
  directly.
repository: facebook/react#b20
label: Code Style
language: TypeScript
comments_count: 4
repository_stars: 251895
---

Favor the simplest construct that accomplishes the goal, and avoid unnecessary indirection, helper abstractions, or parameters when the same result can be expressed directly.

- Simplify conditionals: don't introduce a helper function or complex branching when a direct comparison or ternary suffices. For example, instead of calling `isHyphenatedJsxProp(prop.originalName)` to decide the key, prefer a direct check such as `prop.originalName !== prop.newName ? ... : ...` when it expresses the same intent more simply.
- Avoid passing data that is already accessible through an existing parameter. If a value (e.g. `env`) is reachable via another object already in scope (e.g. `hir.env`), don't add it as a separate function argument.
- Prefer functions that return their result over functions that mutate an output parameter (e.g. writing into a passed-in `Set`/array). Returning a value (or array) and letting the caller merge/assign it makes data flow explicit and the function easier to reason about.
- When building configuration or exported objects, prefer self-contained declarations (e.g. using a `get` accessor) over assigning placeholder values and mutating them afterward, so the final shape is clear at the point of declaration.

Applying these practices keeps functions and modules easier to read, reduces unnecessary surface area, and makes data flow and intent explicit at a glance.