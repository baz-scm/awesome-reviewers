---
title: Use topological sorting
description: When managing dependencies between modules or components, implement a
  topological sorting algorithm to ensure correct initialization order. This prevents
  cascading errors and ensures that dependencies are properly initialized before they're
  used.
repository: nestjs/nest
label: Algorithms
language: TypeScript
comments_count: 3
repository_stars: 71766
---

When managing dependencies between modules or components, implement a topological sorting algorithm to ensure correct initialization order. This prevents cascading errors and ensures that dependencies are properly initialized before they're used.

Key implementation guidelines:
1. Detect and handle circular dependencies
2. When calculating distances between modules, preserve maximum distance when a module is imported by multiple parents
3. Sort modules by dependency order before initialization

Example implementation for updating module distances:

```typescript
// When a module is imported by multiple parents
// always use the maximum possible distance
addRelatedModule(module: Module) {
  this._imports.add(module);
  // Use max to prevent distance regression
  module.distance = Math.max(
    module.distance || 0, 
    this._distance + 1
  );
}
```

This approach ensures stable dependency ordering and prevents initialization issues when components depend on each other. It's particularly important for frameworks where proper initialization sequence directly affects functionality, such as when providers from one module need to be registered before dependent modules can access them.