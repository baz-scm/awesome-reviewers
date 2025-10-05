---
title: defensive null checking
description: Always perform explicit null and undefined checks before accessing object
  properties or methods to prevent runtime errors. This defensive programming approach
  ensures code robustness when dealing with potentially missing data.
repository: TanStack/router
label: Null Handling
language: Markdown
comments_count: 2
repository_stars: 11590
---

Always perform explicit null and undefined checks before accessing object properties or methods to prevent runtime errors. This defensive programming approach ensures code robustness when dealing with potentially missing data.

When working with objects that might be null or undefined, implement multiple layers of validation:

```tsx
const breadcrumbs = matches.map(({ pathname, routeContext }) => {
    if (!routeContext) return null
    if (!('getTitle' in routeContext)) return null
    if (!routeContext.getTitle) return null
    
    return {
        title: routeContext.getTitle(),
        path: pathname,
    }
})
```

This pattern prevents null reference errors by:
1. First checking if the object exists (`!routeContext`)
2. Then verifying the property exists (`'getTitle' in routeContext`)
3. Finally ensuring the method/property is truthy (`!routeContext.getTitle`)

Apply this approach consistently when accessing nested properties, calling methods on potentially undefined objects, or working with data that may not be fully populated. The small overhead of these checks prevents runtime crashes and makes code more reliable.