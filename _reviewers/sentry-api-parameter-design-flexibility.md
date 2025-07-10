---
title: API parameter design flexibility
description: Design API parameters to be extensible and future-proof by using object
  arguments and explicit type definitions instead of boolean flags or simplistic checks.
  This approach makes APIs more maintainable and easier to evolve over time.
repository: getsentry/sentry
label: API
language: TSX
comments_count: 3
repository_stars: 41297
---

Design API parameters to be extensible and future-proof by using object arguments and explicit type definitions instead of boolean flags or simplistic checks. This approach makes APIs more maintainable and easier to evolve over time.

Key principles:
1. Use object parameters instead of individual arguments for functions that might need additional parameters later
2. Prefer string literals over boolean flags for configuration options
3. Implement thorough parameter validation for query parameters

Example:
```typescript
// ❌ Avoid rigid parameter design
function validate(condition: string): string {
  // ...
}

// ✅ Use extensible object parameters
function validate({
  condition,
  context
}: {
  condition: string,
  context?: {
    organization?: string,
    // Easily extendable with new context properties
  }
}): string {
  // ...
}

// ❌ Avoid boolean flags that limit future options
interface ComponentProps {
  fitMaxContent: boolean;
}

// ✅ Use string literals for extensible options
interface ComponentProps {
  fit?: 'max-content' | 'min-content' | 'content'; // Extensible
}
```