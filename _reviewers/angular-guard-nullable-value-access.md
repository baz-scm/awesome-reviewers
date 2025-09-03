---
title: Guard nullable value access
description: Always use appropriate guards or type checks before accessing potentially
  null or undefined values. Prefer type-safe guard methods that provide both runtime
  protection and TypeScript type narrowing over manual null checks.
repository: angular/angular
label: Null Handling
language: Markdown
comments_count: 4
repository_stars: 98611
---

Always use appropriate guards or type checks before accessing potentially null or undefined values. Prefer type-safe guard methods that provide both runtime protection and TypeScript type narrowing over manual null checks.

For Angular resource APIs, use `hasValue()` before accessing `value()` since it acts as both an error guard and type guard that narrows the type to remove `undefined`:

```ts
const firstName = computed(() => {
  if (userResource.hasValue()) {
    // hasValue() guards against errors and narrows type
    return userResource.value().firstName;
  }
  return undefined; // fallback for error/loading states
});
```

For optional component inputs or router data, prefer making inputs required when possible rather than handling undefined throughout your component:

```ts
// Prefer this - required input
settings = input.required<Settings>();

// Over this - optional input requiring null checks
settings = input<Settings>(); // Would need settings()?.theme
```

This pattern prevents runtime errors while leveraging TypeScript's type system to catch potential null reference issues at compile time.