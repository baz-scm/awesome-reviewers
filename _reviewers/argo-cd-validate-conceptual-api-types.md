---
title: validate conceptual API types
description: When defining API types, enums, or interfaces, ensure they represent
  accurate conceptual distinctions within the domain model rather than implementation
  details or delivery mechanisms. Each type should correspond to a meaningful category
  that users and developers can clearly understand and differentiate.
repository: argoproj/argo-cd
label: API
language: TypeScript
comments_count: 2
repository_stars: 20149
---

When defining API types, enums, or interfaces, ensure they represent accurate conceptual distinctions within the domain model rather than implementation details or delivery mechanisms. Each type should correspond to a meaningful category that users and developers can clearly understand and differentiate.

Before adding new values to type unions or enums, verify that the addition represents a true conceptual category. For example, avoid conflating delivery mechanisms (like OCI repositories) with content types (like Helm charts or Kustomize configurations).

Example of problematic type definition:
```typescript
// Problematic - mixes content types with delivery mechanisms
export type AppSourceType = 'Helm' | 'Kustomize' | 'Directory' | 'Plugin' | 'OCI';
```

Example of proper type definition:
```typescript
// Better - focuses on actual source content types
export type AppSourceType = 'Helm' | 'Kustomize' | 'Directory' | 'Plugin';
```

When designing interfaces, include only fields that serve the specific purpose while maintaining conceptual clarity. This approach prevents API confusion and ensures that type definitions remain meaningful and maintainable over time.