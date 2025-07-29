---
title: prefer built-in React types
description: Favor React's built-in types over custom interfaces when possible, and
  consolidate to standard library types for better maintainability and type safety.
  Use `PropsWithChildren` instead of creating custom component prop interfaces, leverage
  generics for type flexibility, and migrate away from deprecated types in favor of
  type-safe alternatives.
repository: remix-run/react-router
label: React
language: TypeScript
comments_count: 4
repository_stars: 55270
---

Favor React's built-in types over custom interfaces when possible, and consolidate to standard library types for better maintainability and type safety. Use `PropsWithChildren` instead of creating custom component prop interfaces, leverage generics for type flexibility, and migrate away from deprecated types in favor of type-safe alternatives.

Example:
```ts
// Instead of custom interface
export interface LayoutComponentProps {
  children: ReactNode
}

// Use built-in React type
export type LayoutComponentProps = PropsWithChildren;

// For additional props, extend with generics
export type LayoutComponentProps = PropsWithChildren<{
  extraProp: string;
}>;

// Use generics for flexibility
export type RouteManifest<R = AgnosticDataRouteObject> = Record<
  string,
  R | undefined
>;
```

This approach reduces code duplication, improves type safety, leverages React's established patterns, and makes the codebase more maintainable by using well-tested standard types.