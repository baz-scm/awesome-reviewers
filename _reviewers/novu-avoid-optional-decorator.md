---
title: avoid @Optional decorator
description: Avoid using the @Optional decorator in NestJS dependency injection as
  it disables runtime DI validation during bootstrap. This can cause missing provider
  dependencies to go undetected during compilation, leading to runtime failures without
  clear error messages.
repository: novuhq/novu
label: NestJS
language: TypeScript
comments_count: 2
repository_stars: 37700
---

Avoid using the @Optional decorator in NestJS dependency injection as it disables runtime DI validation during bootstrap. This can cause missing provider dependencies to go undetected during compilation, leading to runtime failures without clear error messages.

Instead of using @Optional, prefer TypeScript optional properties with the `?` syntax to maintain type safety while preserving NestJS's ability to validate dependencies at startup.

Example:
```typescript
// Avoid - disables DI validation
constructor(
  @Optional()
  private sendWebhookMessage: SendWebhookMessage
) {}

// Prefer - maintains DI validation
constructor(
  private sendWebhookMessage?: SendWebhookMessage
) {}
```

This approach ensures that dependency injection issues are caught early in the development cycle rather than surfacing as obscure runtime errors in production.