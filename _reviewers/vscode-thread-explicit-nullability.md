---
title: Thread explicit nullability
description: When code needs to decide behavior based on “which kind/shape” of a value
  it has, avoid inferring that shape from nullable proxy fields (e.g. `handle !==
  undefined`). Instead, compute the nullability/union-discriminant once at the source
  (where the real value is in scope) and pass an explicit flag or `kind` through a
  DTO. Also ensure your TypeScript types...
repository: microsoft/VSCode
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 194303
---

When code needs to decide behavior based on “which kind/shape” of a value it has, avoid inferring that shape from nullable proxy fields (e.g. `handle !== undefined`). Instead, compute the nullability/union-discriminant once at the source (where the real value is in scope) and pass an explicit flag or `kind` through a DTO. Also ensure your TypeScript types reflect real optionality (`T | undefined`) so runtime checks and contracts stay aligned.

Example pattern:

```ts
// Build the target where you still have the real value.
function buildTargetFromValue(value: unknown): { isStringValue: boolean; handle?: number; resourceUri?: URI } {
  const isStringValue = isStringImplicitContextValue(value);
  return {
    isStringValue,
    handle: isStringValue ? value.handle : undefined,
    resourceUri: isStringValue ? value.resourceUri : undefined,
  };
}

// Consume the explicit flag; do not guess from nullable fields.
function isAlreadyAttached(attachments: readonly IChatRequestVariableEntry[], target: { isStringValue: boolean; handle?: number; resourceUri?: URI }): boolean {
  if (!target.isStringValue) {
    return false;
  }
  // safe to compare handle/resourceUri knowing they came from the same value branch
  return attachments.some(a => a.handle === target.handle && a.resourceUri?.toString() === target.resourceUri?.toString());
}
```

Rules of thumb:
- Compute discriminants/flags once (in the same scope as the original value), then thread them through.
- Don’t treat “field is undefined” as a proxy for “this must be the string-shaped variant” unless that mapping is guaranteed by contract and tested.
- For optional runtime values, model them as `T | undefined` (not as non-optional `T`) and normalize identity inputs consistently (don’t let `undefined`, `null`, and `''` drift across different key-building sites).