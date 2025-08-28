---
title: explicit null handling
description: Use explicit null and undefined checks with assertions to validate assumptions
  and maintain type safety. Prefer `!= null` for checking both null and undefined,
  and use assertions to validate non-null expectations rather than relying on implicit
  checks.
repository: rocicorp/mono
label: Null Handling
language: TypeScript
comments_count: 6
repository_stars: 2091
---

Use explicit null and undefined checks with assertions to validate assumptions and maintain type safety. Prefer `!= null` for checking both null and undefined, and use assertions to validate non-null expectations rather than relying on implicit checks.

Key patterns to follow:

1. **Use explicit undefined checks in type definitions:**
```ts
// Preferred - allows explicitly passing undefined
argv?: string[] | undefined;

// Avoid - implicit undefined handling
argv?: string[];
```

2. **Assert non-null assumptions with clear error messages:**
```ts
// Preferred - explicit assertion
assert(this.#aliveClientsManager !== undefined);
// or
const manager = must(this.#aliveClientsManager);
```

3. **Use consistent null comparison patterns:**
```ts
// Preferred for checking both null and undefined
if (shortID != null) { ... }

// Use when specifically checking undefined
if (issue?.shortID !== undefined) { ... }
```

4. **Handle optional values with fallback patterns:**
```ts
// Preferred - explicit fallback
const permissions = must(this.#permissions).permissions ?? DEFAULT_PERMISSIONS;

// Alternative - short-circuit evaluation
const result = getZeroData && await getZeroData('rebase', hash);
```

This approach prevents runtime null reference errors, makes null handling intentions explicit, and improves code maintainability by clearly documenting assumptions about null/undefined states.