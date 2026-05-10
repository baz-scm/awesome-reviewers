---
title: Deterministic Parse Fallbacks
description: When parsing inputs that may be invalid (e.g., string → boolean), do
  not rely on implicit/unclear failure behavior. Instead, decide explicitly how parse
  errors should be handled and make it deterministic.
repository: colinhacks/zod
label: Error Handling
language: Markdown
comments_count: 2
repository_stars: 42628
---

When parsing inputs that may be invalid (e.g., string → boolean), do not rely on implicit/unclear failure behavior. Instead, decide explicitly how parse errors should be handled and make it deterministic.

Apply this by:
- Using a safe fallback for parse errors (e.g., Zod `.catch(...)`) so invalid values consistently map to a chosen boolean.
- Ensuring the parsing semantics match your intent: `z.string().boolean()` uses logical string values (like "true"/"false"), which may differ from TypeScript/JS `Boolean()` behavior—use `z.coerce.boolean()` when you want coercion semantics.

Example (explicit error recovery to a boolean):
```ts
import { z } from "zod";

// Logical boolean parsing with deterministic fallback on error
const b = z.string()
  .boolean()
  .catch(() => false); // whenever parsing fails

b.parse("true");   // true
b.parse("False");  // false
b.parse("other");  // false (fallback)
```

If you expect JS-like coercion semantics instead of strict logical strings, prefer:
```ts
const b = z.coerce.boolean();
```