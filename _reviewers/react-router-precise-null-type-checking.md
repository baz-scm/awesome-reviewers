---
title: precise null type checking
description: Use precise null and undefined type checking that matches the actual
  usage context. Distinguish between checking if a type contains undefined (`undefined
  extends T`) versus checking if a type is exactly undefined (`Equal<T, undefined>
  extends true`). For inferred return types, use the "contains undefined" check since
  the type may be a union. For direct...
repository: remix-run/react-router
label: Null Handling
language: TypeScript
comments_count: 6
repository_stars: 55270
---

Use precise null and undefined type checking that matches the actual usage context. Distinguish between checking if a type contains undefined (`undefined extends T`) versus checking if a type is exactly undefined (`Equal<T, undefined> extends true`). For inferred return types, use the "contains undefined" check since the type may be a union. For direct values and top-level parameters, use exact equality checks.

Additionally, ensure optional modifiers in type definitions match actual implementation requirements. Remove optional modifiers (`?`) when parameters are required in the implementation, and use precise typing to distinguish required parameters (`string`) from optional ones (`string | null | undefined`).

Example of precise undefined checking:
```typescript
// For inferred types - check if undefined is in the union
type IsDefined<T> = undefined extends T ? false : true;

// For exact values - check if type is exactly undefined  
type IsExactlyUndefined<T> = Equal<T, undefined> extends true ? false : true;

// Distinguish required vs optional parameters
type PathParams<Path> = {
  [key in RequiredPathParam<Path>]: string;
} & {
  [key in OptionalPathParam<Path>]?: string | null | undefined;
};

// Remove optional modifier when parameter is actually required
getFetcher<TData = any>(key: string): Fetcher<TData>; // not key?: string
```

This approach prevents type errors, ensures API contracts match implementations, and provides better developer experience through more accurate IntelliSense and compile-time checking.