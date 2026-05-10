---
title: Guard nullable inputs
description: 'When a value can be `undefined`/`null`, do not assume it exists—guard
  it before access and keep the type model consistent.


  **Rules**

  - Use optional chaining / nullish guards when reading fields from optional params:'
repository: colinhacks/zod
label: Null Handling
language: TypeScript
comments_count: 7
repository_stars: 42628
---

When a value can be `undefined`/`null`, do not assume it exists—guard it before access and keep the type model consistent.

**Rules**
- Use optional chaining / nullish guards when reading fields from optional params:
  ```ts
  function f(params?: { message?: string | ((d: unknown[]) => string) }) {
    const message =
      typeof params?.message === "function"
        ? params.message
        : errorUtil.toString(params?.message);
  }
  ```
- Before using `in`, `Object.keys`, or nested properties, ensure the container object exists:
  ```ts
  if (refSeen.def && key in refSeen.def) {
    // safe
  }
  ```
- If a value is not actually optional, don’t add optional parameters/fallbacks—prefer required types (avoid “unnecessary undefined handling”).
- If you convert invalid data to `undefined` (e.g., coercion failures), make sure downstream code treats that `undefined` as the expected “invalid” state and update types accordingly.
- Be consistent in how you model “missing” vs “present but undefined” in types; adding `: undefined` can change runtime semantics (`"prop" in obj`). Prefer property absence when that’s the intended meaning.

**Outcome**: fewer runtime `TypeError`s and clearer, more intentional null/undefined handling across the codebase.