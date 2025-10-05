---
title: API parameter design
description: Design API parameters thoughtfully by making them optional when appropriate,
  avoiding unnecessary required parameters, and maintaining backward compatibility
  when changing parameter signatures. Consider the actual usage patterns and avoid
  forcing users to provide parameters that have sensible defaults or aren't always
  needed.
repository: TanStack/router
label: API
language: TypeScript
comments_count: 6
repository_stars: 11590
---

Design API parameters thoughtfully by making them optional when appropriate, avoiding unnecessary required parameters, and maintaining backward compatibility when changing parameter signatures. Consider the actual usage patterns and avoid forcing users to provide parameters that have sensible defaults or aren't always needed.

Key principles:
- Make parameters optional when they have reasonable defaults or aren't always required
- Avoid breaking changes by preserving existing parameter signatures when possible
- Remove unnecessary parameters that add complexity without value
- Ensure all documented parameters actually work as intended

Example of good parameter design:
```ts
// Before: forcing unnecessary required parameter
interface MatchRoutesFn {
  (pathname: string, locationSearch: AnySchema) // always required
}

// After: making parameter optional when it has defaults
interface MatchRoutesFn {
  (pathname: string, locationSearch?: AnySchema) // optional when not needed
}

// Before: passing unnecessary parameters
navigate: (opts: any) => this.navigate({ ...opts, from: match.pathname })

// After: removing unnecessary complexity  
navigate: (opts: any) => this.navigate(opts)
```

This approach reduces API surface area, improves developer experience, and prevents breaking changes that force users to update working code unnecessarily.