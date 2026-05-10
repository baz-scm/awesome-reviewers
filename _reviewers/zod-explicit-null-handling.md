---
title: Explicit null handling
description: 'Treat `null`/`undefined` and “absence vs presence” as first-class concerns.


  - **TypeScript:** Keep null safety effective by ensuring `strictNullChecks` is enabled
  and not overridden by extended configs (explicitly set it to `true` if needed).'
repository: colinhacks/zod
label: Null Handling
language: Markdown
comments_count: 3
repository_stars: 42628
---

Treat `null`/`undefined` and “absence vs presence” as first-class concerns.

- **TypeScript:** Keep null safety effective by ensuring `strictNullChecks` is enabled and not overridden by extended configs (explicitly set it to `true` if needed).
- **Zod runtime:** Decide what should happen when input is `undefined` vs when it is a wrong value or `null`.
  - Use **`.default(value)`** for **absent** inputs (typically `undefined`).
  - Use **`.catch(fallback)`** for **parsing failures** (including wrong strings), not as a substitute for handling `undefined`.
- **Form inputs:** Don’t assume “required field” means “non-empty”. Browsers/DOM often send `""` for an “empty” required field; `z.string()` will accept `""` as a valid string. If you require non-empty content, validate it explicitly (e.g., `.min(1)`).

Example:
```ts
import { z } from "zod";

const boolSchema = z.string().boolean();

// absent (undefined) -> fallback
const withDefault = boolSchema.default(false);

// wrong value (including "other" / null if you pass it in) -> fallback
const withCatch = boolSchema.catch(false);

// non-empty string required by UI
const requiredText = z.string().min(1, "Required");
```

Apply these consistently so validation behavior matches what your types and UI expectations actually mean.