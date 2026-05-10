---
title: Define Validation Contracts
description: 'When adding/maintaining API validation schemas, make the input contract
  explicit: specify exactly what input types are accepted, and whether the schema
  is parsing (strict mapping) or coercing/converting values. Don’t rely on assumptions
  about built-in JS semantics or on a single runtime’s concrete types.'
repository: colinhacks/zod
label: API
language: Markdown
comments_count: 4
repository_stars: 42628
---

When adding/maintaining API validation schemas, make the input contract explicit: specify exactly what input types are accepted, and whether the schema is parsing (strict mapping) or coercing/converting values. Don’t rely on assumptions about built-in JS semantics or on a single runtime’s concrete types.

Apply these rules:
- **Boolean:** If the API accepts boolean-like strings, confirm the semantics. `z.string().boolean()` does *not* match `Boolean()`/MDN behavior—use `z.coerce.boolean()` when you want JS `Boolean()`-style coercion.
- **Dates:** Use `z.date()` only for actual `Date` objects. If the API accepts date strings too, explicitly convert via `z.preprocess`.
- **Cross-runtime files:** Don’t couple validation to “browser File only” if your API is used in Node/Deno too. Validate a shared file **contract** (e.g., `size`, `type`, etc.) or create separate schemas per runtime.
- **Deprecations:** Avoid deprecated Zod helpers in public schemas; use current equivalents (e.g., `z.string().min(1)` instead of deprecated `nonempty`).

Example (date + boolean semantics):
```ts
import { z } from "zod";

// Dates: accept both Date and ISO strings
const dateSchema = z.preprocess((arg) => {
  if (typeof arg === "string" || arg instanceof Date) return new Date(arg);
}, z.date());

// Booleans: choose semantics explicitly
const strictLogicalBool = z.string().boolean(); // accepts specific strings like "TRUE"/"False"
const jsBooleanLike = z.coerce.boolean();       // matches JS Boolean() coercion semantics
```
