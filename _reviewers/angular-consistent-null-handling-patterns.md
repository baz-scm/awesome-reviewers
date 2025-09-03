---
title: consistent null handling patterns
description: Use consistent and meaningful null/undefined handling patterns throughout
  your code. Prefer positive type guards over negated early returns, maintain consistency
  between null and undefined return types, and be careful with optional chaining semantics.
repository: angular/angular
label: Null Handling
language: TypeScript
comments_count: 8
repository_stars: 98611
---

Use consistent and meaningful null/undefined handling patterns throughout your code. Prefer positive type guards over negated early returns, maintain consistency between null and undefined return types, and be careful with optional chaining semantics.

Key practices:
1. **Use positive conditionals**: Instead of `if (!ts.isIdentifier(node.name)) return;`, use `if (ts.isIdentifier(node.name)) { ... } else if (ts.isObjectBindingPattern(node.name)) { ... }`

2. **Consistent return types**: Choose either `null` or `undefined` consistently for similar functions. For example, prefer `return null` over `return undefined` when indicating "no result found".

3. **Careful optional chaining**: Understand semantic differences between `document?.documentElement?.getAnimations` and explicit checks. Optional chaining can still throw if the base object is undefined in some contexts.

4. **Derive state from data presence**: Instead of manually managing loading states, derive them from whether data exists: `const isLoading = computed(() => !this.transferStateData() && !this.error())`

5. **Meaningful null/undefined**: Use null/undefined to represent meaningful states like "no constraint applies" or "validation skipped" rather than just absence of data.

Example of improved null handling:
```typescript
// Before: Negated early return
if (!ts.isIdentifier(node.name)) {
  return;
}

// After: Positive conditionals with explicit handling
if (ts.isIdentifier(node.name)) {
  migrateIdentifierParameter(context);
} else if (ts.isObjectBindingPattern(node.name)) {
  migrateObjectBindingParameter(context);
} else {
  return;
}
```