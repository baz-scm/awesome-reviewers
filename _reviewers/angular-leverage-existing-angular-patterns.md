---
title: leverage existing Angular patterns
description: Before implementing new functionality, check if Angular already provides
  a suitable utility, service, or pattern that can be reused. This promotes consistency
  across the codebase, reduces duplication, and follows established Angular conventions.
repository: angular/angular
label: Angular
language: TypeScript
comments_count: 6
repository_stars: 98611
---

Before implementing new functionality, check if Angular already provides a suitable utility, service, or pattern that can be reused. This promotes consistency across the codebase, reduces duplication, and follows established Angular conventions.

Key areas to check:
- **Services and utilities**: Use existing services like `Clipboard` service instead of implementing custom clipboard functionality
- **API patterns**: Follow established patterns like using `ng` global APIs for devtools functionality rather than creating new approaches
- **Injection tokens**: Use factory functions in injection tokens with default implementations instead of separate providers
- **Built-in functions**: Reuse existing functions like `retrieveTransferredState()` instead of reimplementing similar logic

Example of good practice:
```typescript
// Instead of custom clipboard implementation
async copyToClipboard(text: string) {
  await navigator.clipboard.writeText(text);
}

// Use Angular's Clipboard service
constructor(private clipboard = inject(Clipboard)) {}
copyToClipboard(text: string) {
  this.clipboard.copy(text);
}

// Instead of separate provider
export const WINDOW_PROVIDER: Provider = {
  provide: WINDOW,
  useValue: window,
};

// Use factory in token definition
export const WINDOW = new InjectionToken<Window>('WINDOW', {
  factory: () => window,
});
```

This approach ensures better maintainability, leverages Angular's built-in optimizations, and provides a more consistent developer experience.