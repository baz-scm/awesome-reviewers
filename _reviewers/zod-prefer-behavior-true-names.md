---
title: Prefer behavior-true names
description: Use naming that clearly communicates the real behavior/intent of the
  API and avoids misleading abbreviations or borrowed terms whose common meaning differs.
repository: colinhacks/zod
label: Naming Conventions
language: Markdown
comments_count: 3
repository_stars: 42628
---

Use naming that clearly communicates the real behavior/intent of the API and avoids misleading abbreviations or borrowed terms whose common meaning differs.

Apply this when adding/renaming methods:
- Match semantics to behavior: if the method “checks and returns input as-is,” don’t name it after an operation that “returns an array without duplicates.”
- Prefer full, intention-revealing names over short/ambiguous ones when they reduce clarity.
- If a common ecosystem term may imply different semantics, choose a name that reflects the actual operation (or explicitly document the difference).
- For domain terms that overlap with other systems (e.g., “forms”), ensure the wording/dox strings align with the library’s/TypeScript’s meaning to prevent confusion.

Example rule in practice:
- ❌ Confusing due to semantic mismatch: a method named like lodash `uniq` when it does not dedupe/transform.
- ✅ Clearer alternative: choose a name that reflects what happens (e.g., “unique/ distinct” only if the operation truly enforces/derives uniqueness as that name implies), or pick another verb that matches intent (as in the naming exploration for `.check`).
