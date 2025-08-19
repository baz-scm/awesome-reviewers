---
title: Leverage TypeScript null safety
description: Use TypeScript's type system proactively to prevent null and undefined
  issues at compile time rather than handling them reactively at runtime. This includes
  using exhaustive pattern matching, explicit type annotations, and avoiding type
  casting that can hide null safety problems.
repository: browserbase/stagehand
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 16443
---

Use TypeScript's type system proactively to prevent null and undefined issues at compile time rather than handling them reactively at runtime. This includes using exhaustive pattern matching, explicit type annotations, and avoiding type casting that can hide null safety problems.

Key practices:
- Use switch statements with exhaustive matching to ensure all cases are handled: `default: { throw exhaustiveMatchingGuard(action); }`
- Provide explicit type annotations for complex types instead of relying on type casting: `const result: AnthropicTransformedResponse` instead of `return result as T`
- Handle null values explicitly with proper fallbacks: `const xpaths = elementId === null ? ["//body"] : selectorMap[elementId] ?? [];`
- Use proper array typing to prevent undefined access: `Array<{ input: EvalInput; output?: boolean }>` instead of generic arrays

Example of good null safety:
```typescript
// Instead of type casting that hides null issues
return cachedResponse as T;

// Use explicit typing
const cachedResponse: AnthropicTransformedResponse | undefined = this.cache.get(...);
if (cachedResponse) {
  return cachedResponse;
}
```

This approach catches potential null/undefined issues during development rather than discovering them at runtime.