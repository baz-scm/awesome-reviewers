---
title: Use factory providers
description: Prefer `useFactory` over `useValue` when registering providers, especially
  for large objects or complex configurations. This improves application performance
  by avoiding unnecessary serialization during the dependency injection process.
repository: nestjs/nest
label: NestJS
language: Typescript
comments_count: 4
repository_stars: 71766
---

Prefer `useFactory` over `useValue` when registering providers, especially for large objects or complex configurations. This improves application performance by avoiding unnecessary serialization during the dependency injection process.

When using `useValue`, NestJS must serialize and hash the entire object to create a unique token, which can be computationally expensive for large objects. Using `useFactory` avoids this overhead as functions are not deeply serialized.

**Instead of this:**
```typescript
{
  provide: MULTER_MODULE_OPTIONS,
  useValue: options,  // Options object could be large or complex
}
```

**Do this:**
```typescript
{
  provide: MULTER_MODULE_OPTIONS,
  useFactory: () => options,  // Function reference is lightweight
}
```

This approach is particularly important when:
1. The provided value is a large object with many properties
2. The value contains circular references
3. You're registering multiple modules with similar configurations

For modules that need unique identities, consider using the `UniqueDynamicModuleFactory` to avoid hash generation altogether:

```typescript
UniqueDynamicModuleFactory.wrap('my-unique-id', dynamicModule);
```

This performance optimization can significantly reduce bootstrap time for applications with many modules and complex configurations.