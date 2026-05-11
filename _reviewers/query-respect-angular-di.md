---
title: Respect Angular DI
description: 'When integrating with Angular’s DI and reactivity, follow these rules:


  - **Dependency access:** For hook-like utilities, accept an optional **Injector**
  (or injector-derived path) so the function can be executed both **inside and outside**
  the normal injection context. Use Angular’s injection-context/assert-injector helpers
  to resolve dependencies from the...'
repository: tanstack/query
label: Angular
language: TypeScript
comments_count: 6
repository_stars: 49380
---

When integrating with Angular’s DI and reactivity, follow these rules:

- **Dependency access:** For hook-like utilities, accept an optional **Injector** (or injector-derived path) so the function can be executed both **inside and outside** the normal injection context. Use Angular’s injection-context/assert-injector helpers to resolve dependencies from the Injector when provided.
- **Effect lifecycle + teardown:** If you use `effect(...)` to keep signals in sync, add/propagate **cleanup** via the effect `onCleanup` argument wherever long-lived listeners/subscriptions are created.
- **Signal write semantics:** If an effect updates a signal, ensure signal writes follow Angular’s expectations: use `allowSignalWrites: true` and wrap option reads in `untracked` when needed to avoid unintended tracking loops.
- **Modern HTTP interceptors:** Prefer **functional interceptors** via `withInterceptors(...)` over DI-provided interceptor classes. Also avoid redundant `HttpClientModule` wiring when using `provideHttpClient(...)`.

Example pattern for effect-driven signal updates:
```ts
import { DestroyRef, effect, inject, signal, untracked, type Injector } from '@angular/core';

export function injectSomething(optionsFn = () => ({}), injector?: Injector) {
  // resolve dependencies from injector / injection context here
  return ((): any => {
    const destroyRef = inject(DestroyRef);
    const value = signal(0);

    effect(
      () => {
        const opts = untracked(() => optionsFn());
        // imperative signal update inside effect
        value.set(opts.someValue);
      },
      { allowSignalWrites: true }
    );

    return value;
  })();
}
```

Applying this set of practices will make utilities safer to use across injection contexts, reduce lifecycle leaks, and align with Angular’s current HTTP interceptor direction.