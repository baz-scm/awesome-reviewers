---
title: optimize file-based routing
description: Implement lazy loading patterns and strategic code-splitting in file-based
  routing systems to improve performance and reduce unnecessary processing. Root routes
  should never be code-split since they're always needed, while other routes can benefit
  from lazy instantiation to avoid parsing route trees when not required.
repository: TanStack/router
label: Next
language: TypeScript
comments_count: 2
repository_stars: 11590
---

Implement lazy loading patterns and strategic code-splitting in file-based routing systems to improve performance and reduce unnecessary processing. Root routes should never be code-split since they're always needed, while other routes can benefit from lazy instantiation to avoid parsing route trees when not required.

Key strategies:
1. Use lazy instantiation for route parsing to defer expensive operations until actually needed
2. Exclude root routes from code-splitting since they're always required
3. Add clear comments explaining routing optimization decisions for future maintainers

Example implementation:
```typescript
// Use lazy instantiation pattern for route parsing
export type CodeRoutesByPath<TRouteTree extends AnyRoute> =
  ParseRoute<TRouteTree> extends infer TRoutes extends AnyRoute
  
// Skip code-splitting for root routes with explanatory comment
if (createRouteFn !== 'createFileRoute') {
  // Exit early for root routes since they are never code-split
  // Root routes are always needed and should remain in the main bundle
  return
}
```

This approach aligns with Next.js principles of file-based routing optimization and incremental static regeneration by ensuring only necessary code is loaded when needed while maintaining fast initial page loads.