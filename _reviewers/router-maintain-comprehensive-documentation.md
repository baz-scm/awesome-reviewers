---
title: Maintain comprehensive documentation
description: 'When making code changes, ensure all relevant documentation is updated
  comprehensively across different formats and locations. This includes:


  1. **JSDoc comments** for functions, especially internal APIs that need usage context'
repository: TanStack/router
label: Documentation
language: TypeScript
comments_count: 5
repository_stars: 11590
---

When making code changes, ensure all relevant documentation is updated comprehensively across different formats and locations. This includes:

1. **JSDoc comments** for functions, especially internal APIs that need usage context
2. **Inline comments** for complex logic sections to aid future maintainers  
3. **External markdown documentation** when adding new API properties or references
4. **Clear test expectations** that explicitly show expected transformations

For example, when adding a new function:
```typescript
/**
 * @internal
 * Handles hash-based scrolling during route transitions.
 * Should be setup in the `<Transitioner>` component.
 */
export function handleTransitionerHashScroll(router: AnyRouter) {
  // Actually fire off the `beforeLoad` callback
  const beforeLoadContext = await route.options.beforeLoad?.(beforeLoadFnContext)
}
```

And ensure corresponding updates to:
- API documentation files (e.g., `RouterOptionsType.md`, `RouterType.md`)
- External reference links (MDN, etc.) in markdown files
- Test cases with explicit expected values rather than computed ones

This comprehensive approach ensures that documentation remains synchronized with code changes and provides clear guidance for future developers.