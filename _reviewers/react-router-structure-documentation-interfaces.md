---
title: Structure documentation interfaces
description: Organize interfaces and component props documentation to improve API
  clarity and maintainability. Extract reusable interfaces into separate declarations
  to generate dedicated documentation pages, and ensure prop documentation accurately
  represents the code structure, especially for rest/spread operators.
repository: remix-run/react-router
label: Documentation
language: TSX
comments_count: 2
repository_stars: 55270
---

Organize interfaces and component props documentation to improve API clarity and maintainability. Extract reusable interfaces into separate declarations to generate dedicated documentation pages, and ensure prop documentation accurately represents the code structure, especially for rest/spread operators.

When documenting components with rest/spread props, clearly indicate they represent collections of properties rather than individual parameters. Avoid documenting every individual property when they map to standard web APIs - instead, reference the appropriate external documentation.

```tsx
// Good: Extract interface for dedicated docs page
export interface MemoryRouterOpts {
  initialEntries?: string[];
  initialIndex?: number;
}

// Good: Clear rest/spread documentation
/**
 * @param props.dataLinkProps Additional props to pass to the
 * underlying link elements (collection of standard HTML attributes)
 */
function PrefetchPageLinks({ page, ...dataLinkProps }: Props) {
  // Implementation
}
```

This approach ensures documentation is well-organized, technically accurate, and provides appropriate level of detail without duplicating standard web API documentation.