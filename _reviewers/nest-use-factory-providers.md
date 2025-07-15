---
title: Use factory providers
description: Prefer `useFactory` over `useValue` for better performance in NestJS
  dependency injection, especially for large objects or complex configurations. Using
  `useValue` with large objects can significantly slow down application bootstrapping
  due to expensive module serialization.
repository: nestjs/nest
label: NestJS
language: TypeScript
comments_count: 3
repository_stars: 71767
---

Prefer `useFactory` over `useValue` for better performance in NestJS dependency injection, especially for large objects or complex configurations. Using `useValue` with large objects can significantly slow down application bootstrapping due to expensive module serialization.

When defining providers in a module, implement them as factory functions:

```typescript
// Less optimal - may cause performance issues with large objects
{ 
  provide: MULTER_MODULE_OPTIONS, 
  useValue: complexConfigObject 
}

// Better performance
{ 
  provide: MULTER_MODULE_OPTIONS, 
  useFactory: () => complexConfigObject 
}
```

This optimization prevents deep serialization of object structures during module token creation. The serialization process in NestJS needs to stringify providers to create unique identifiers, and complex objects can significantly impact performance.

If your application has slow startup times, check for warnings about module serialization exceeding 10ms, which indicates potential performance bottlenecks. Converting value providers to factory providers can substantially reduce initialization time in larger applications with complex dependency graphs.