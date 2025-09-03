---
title: API consistency patterns
description: Ensure that similar APIs follow consistent patterns and conventions across
  the codebase. When designing or modifying APIs, maintain the same expressivity,
  return type patterns, and usage conventions as existing similar APIs.
repository: angular/angular
label: API
language: TypeScript
comments_count: 5
repository_stars: 98611
---

Ensure that similar APIs follow consistent patterns and conventions across the codebase. When designing or modifying APIs, maintain the same expressivity, return type patterns, and usage conventions as existing similar APIs.

Key areas to check:
- **Return type consistency**: Use established patterns like `OneOrMany<T>` consistently across similar APIs rather than mixing single values and arrays arbitrarily
- **Expressivity consistency**: Ensure similar API handlers have the same capabilities (e.g., "animation event handlers should have the same expressivity/shape as normal event handlers")
- **Usage pattern consistency**: Provide uniform ways to create and use similar constructs (e.g., always use static factory methods rather than mixing constructors and factories)
- **Import consistency**: Export related functionality from the same public API entry points
- **Behavioral consistency**: Apply the same logic across similar use cases rather than having different behaviors for equivalent scenarios

Example from the codebase:
```typescript
// Inconsistent - mixing different return patterns
function someApi(): ValidationError | ValidationError[] // inconsistent with other APIs

// Consistent - following established OneOrMany pattern  
function someApi(): OneOrMany<ValidationError> // matches other similar APIs

// Inconsistent - different creation patterns
new ReactiveMetadataKey() vs MetadataKey.someFactory()

// Consistent - uniform factory pattern
MetadataKey.reduce() // always use static factories
```

This helps users build intuitive mental models and reduces cognitive load when working with related APIs.