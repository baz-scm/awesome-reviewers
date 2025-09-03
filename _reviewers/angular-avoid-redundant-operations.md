---
title: avoid redundant operations
description: Identify and eliminate redundant computations, function calls, and expensive
  operations that can be cached, memoized, or combined. This includes avoiding repeated
  function invocations with the same parameters, caching expensive calculations, and
  combining multiple operations that access the same data.
repository: angular/angular
label: Performance Optimization
language: TypeScript
comments_count: 5
repository_stars: 98611
---

Identify and eliminate redundant computations, function calls, and expensive operations that can be cached, memoized, or combined. This includes avoiding repeated function invocations with the same parameters, caching expensive calculations, and combining multiple operations that access the same data.

Examples of optimization opportunities:
- Cache expensive function results: Instead of calling `getComponentDef(instance.constructor)` multiple times, store the result in a variable
- Combine related operations: Merge `isAnimationRunning` and `cancelAnimations` functions to avoid duplicate animation lookups
- Extract static objects: Move objects and functions that don't depend on method parameters outside the method to avoid recreation on each call
- Use memoization: For expensive logic functions that may be called repeatedly with the same inputs, consider using computed signals or manual caching

```typescript
// Before: Redundant function calls
function componentUsesShadowDomEncapsulation(lView: LView): boolean {
  const instance = lView[CONTEXT];
  return instance?.constructor
    ? getComponentDef(instance.constructor)?.encapsulation === ViewEncapsulation.ShadowDom ||
        getComponentDef(instance.constructor)?.encapsulation === ViewEncapsulation.IsolatedShadowDom
    : false;
}

// After: Cache the result
function componentUsesShadowDomEncapsulation(lView: LView): boolean {
  const instance = lView[CONTEXT];
  if (!instance?.constructor) return false;
  
  const componentDef = getComponentDef(instance.constructor);
  return componentDef?.encapsulation === ViewEncapsulation.ShadowDom ||
         componentDef?.encapsulation === ViewEncapsulation.IsolatedShadowDom;
}
```

This optimization reduces computational overhead, improves runtime performance, and can significantly impact applications with frequent function calls or expensive operations.