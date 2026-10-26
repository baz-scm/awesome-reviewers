---
title: Normalize Nulls Safely
description: 'At system boundaries, normalize and validate nullable inputs immediately—treat
  `null` and `undefined` as distinct representations only if you can prove they must
  behave differently. Otherwise: convert to a single canonical meaning (often “omitted”),
  make precedence explicit, and avoid fallthrough when a value that “should exist”
  is missing.'
repository: cline/cline#v2
label: Null Handling
language: TypeScript
comments_count: 7
repository_stars: 70861
---

At system boundaries, normalize and validate nullable inputs immediately—treat `null` and `undefined` as distinct representations only if you can prove they must behave differently. Otherwise: convert to a single canonical meaning (often “omitted”), make precedence explicit, and avoid fallthrough when a value that “should exist” is missing.

Practical rules:
- **Normalize early:** If downstream logic treats absence as omission, convert `null` → `undefined`/omit (e.g., for create/insert style operations) and keep runtime/typing aligned.
- **Encode precedence explicitly:** When both legacy and new flags exist, define and implement a clear winner (e.g., `disabled: true` overrides `enabled: false`). Don’t rely on “truthy/falsey” or object merge order.
- **Type invariants:** If a field is only valid in certain lifecycle phases, model that in TypeScript so impossible states don’t compile.
- **Fail fast on impossible-missing:** If a “should never be null” value is missing after required steps, throw rather than continuing into a path that can silently corrupt state.

Example (frontmatter precedence + boolean coercion):
```ts
export function isFrontmatterDisabled(data: Record<string, unknown>): boolean {
  // disabled: true wins
  if (typeof data.disabled === "boolean") return data.disabled;
  // enabled: false only counts when disabled is absent
  return data.enabled === false;
}
```

Example (normalize `null` to omission):
```ts
function normalizeOptionalString(v: string | null | undefined): string | undefined {
  return typeof v === "string" ? v : undefined; // null/undefined => omitted
}
```