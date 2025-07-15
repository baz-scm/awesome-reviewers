---
title: Optimize critical path iterations
description: 'Use appropriate iteration techniques in performance-critical code paths
  to minimize overhead and maximize execution speed:


  1. **Use raw for loops with early termination** instead of array methods like `map`
  and `filter` for maximum performance:'
repository: nestjs/nest
label: Performance Optimization
language: TypeScript
comments_count: 3
repository_stars: 71767
---

Use appropriate iteration techniques in performance-critical code paths to minimize overhead and maximize execution speed:

1. **Use raw for loops with early termination** instead of array methods like `map` and `filter` for maximum performance:

```javascript
// Less performant
return methods
  .map(methodKey => this.exploreMethodMetadata(instance, instancePrototype, methodKey))
  .filter(route => route !== undefined);

// More performant
const routes = [];
for (const methodKey of methods) {
  const route = this.exploreMethodMetadata(instance, instancePrototype, methodKey);
  if (!route) continue;
  routes.push(route);
}
return routes;
```

2. **Consider `reduce` as a middle ground** between readability and performance when appropriate.

3. **Move invariant calculations outside loops and callbacks** to prevent redundant executions:

```javascript
// Less performant
function callback() {
  const isTreeDurable = wrapper.isDependencyTreeDurable(); // Executed on each call
  // ...
}

// More performant
const isTreeDurable = wrapper.isDependencyTreeDurable(); // Executed once
function callback() {
  // ...
}
```

4. **Break loops early** when the goal has been achieved:

```javascript
// Less performant (processes all items)
return this.getAll(metadataKey, targets).find(item => item !== undefined);

// More performant (stops at first match)
for (const target of targets) {
  const result = this.get(metadataKey, target);
  if (result !== undefined) {
    return result;
  }
}
return undefined;
```

For critical code paths, benchmark different approaches with realistic data volumes to confirm performance benefits before sacrificing readability.