---
title: Scope-Aware Name Sanitization
description: When code transforms external strings (JSX attribute/tag names, object
  keys) into internal identifiers, enforce naming rules that are (a) validity-aware,
  (b) scope-safe for uniqueness, and (c) precisely documented.
repository: facebook/react#b16
label: Naming Conventions
language: TypeScript
comments_count: 3
repository_stars: 251891
---

When code transforms external strings (JSX attribute/tag names, object keys) into internal identifiers, enforce naming rules that are (a) validity-aware, (b) scope-safe for uniqueness, and (c) precisely documented.

Apply this standard:
1) **Check identifier validity before generating identifiers.** If it’s not a valid JS identifier (e.g. `aria-label`), either transform it deterministically (e.g. camelCase) or handle it via an explicit representation.
2) **Generate uniqueness from the correct scope boundary.** If you rely on dedup sets like `seen`, ensure they cover the full collision domain you care about. Otherwise prefer the scope/program-context mechanism (e.g. `programContext.newUuid()` / `newUid`) designed to avoid collisions.
3) **Avoid coercing non-identifier cases into identifier-looking strings unless that’s explicitly modeled.** If you encounter something like a numeric object key, consider representing it directly (or via a clear enum/variant) rather than forcing `String(value)` into an identifier name without documenting the intent.
4) **Keep comments accurate to parser guarantees.** If the parser guarantees only valid identifiers reach a branch, say “valid identifiers” (not “all identifiers”).

Example pattern (safe prop-name sanitization):
```ts
function sanitizePropName(originalName: string, ctx: ProgramContext, scopeKey: string): string {
  if (isValidIdentifier(originalName)) return originalName;
  const base = originalName
    .replace(/[^a-zA-Z0-9$_]+(.)?/g, (_, ch) => (ch ? ch.toUpperCase() : ''));
  // Prefer scope-safe UUID/name generation for the target fresh scope.
  return ctx.newUid(`${base || '_'}`) /* or ctx.newUuid(base) depending on API */;
}
```

This prevents accidental over/under-renaming, avoids collisions, and ensures identifier-related comments remain truthful.