---
title: leverage TypeScript nullability
description: When dealing with values that may be null or undefined, explicitly leverage
  TypeScript's nullable types to identify dependencies and guide null handling decisions.
  Make values nullable when their availability is uncertain, then let TypeScript reveal
  where null checks are needed.
repository: block/goose
label: Null Handling
language: TypeScript
comments_count: 2
repository_stars: 19037
---

When dealing with values that may be null or undefined, explicitly leverage TypeScript's nullable types to identify dependencies and guide null handling decisions. Make values nullable when their availability is uncertain, then let TypeScript reveal where null checks are needed.

For runtime scenarios where the type system cannot guarantee non-null values (like providers or external dependencies), use defensive null checks with optional chaining:

```typescript
// When type system can't guarantee non-null at runtime
if (chatContext?.setRecipeParameters) {
  chatContext.setRecipeParameters(inputValues);
}
```

For values you control, make them explicitly nullable and let TypeScript guide you to handle all null cases:

```typescript
// Make uncertain values explicitly nullable
let pid: number | null;
// TypeScript will now enforce null checks wherever pid is used
```

This approach combines the safety of explicit nullable types with defensive programming for runtime uncertainties, ensuring comprehensive null handling coverage.