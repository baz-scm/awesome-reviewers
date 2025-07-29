---
title: API backward compatibility
description: When evolving APIs, maintain backward compatibility by preserving existing
  public interfaces while adding new functionality through internal implementations
  or optional parameters. Avoid breaking changes that remove functionality without
  providing migration paths.
repository: remix-run/react-router
label: API
language: TSX
comments_count: 4
repository_stars: 55270
---

When evolving APIs, maintain backward compatibility by preserving existing public interfaces while adding new functionality through internal implementations or optional parameters. Avoid breaking changes that remove functionality without providing migration paths.

Key principles:
- Fork internal implementations to expand functionality without changing public APIs
- Support both old and new API patterns during transition periods  
- Make internal utilities public when they provide value to external users
- Use optional parameters and function overloads to extend APIs gracefully

Example from the codebase:
```typescript
// Good: Internal fork preserves public API
export function renderMatches(matches: RouteMatch[] | null): React.ReactElement | null {
  // Internal _renderMatches was forked to allow data-router capabilities
  // without changing the existing renderMatches public API
}

// Bad: Breaking change removes functionality
export function createRoutesStub(
  routes: StubRouteObject[],
  unstable_getContext?: () => unstable_InitialContext  // Used to take AppLoadContext
) {
  // This breaks existing usage - should support both types
}

// Better: Support both patterns
export function createRoutesStub(
  routes: StubRouteObject[],
  contextOrGetter?: AppLoadContext | (() => unstable_InitialContext)
)
```

Consider exposing internal utilities as public APIs when they solve common user problems, such as middleware pipeline utilities for custom data strategies.