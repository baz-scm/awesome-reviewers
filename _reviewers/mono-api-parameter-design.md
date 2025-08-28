---
title: API parameter design
description: 'When designing API functions and types, prioritize maintainability and
  extensibility through proper parameter and type design patterns.


  For functions with multiple parameters, especially multiple boolean flags, consolidate
  them into a single options object to improve readability and future extensibility.
  This prevents parameter lists from becoming unwieldy...'
repository: rocicorp/mono
label: API
language: TSX
comments_count: 2
repository_stars: 2091
---

When designing API functions and types, prioritize maintainability and extensibility through proper parameter and type design patterns.

For functions with multiple parameters, especially multiple boolean flags, consolidate them into a single options object to improve readability and future extensibility. This prevents parameter lists from becoming unwieldy and makes the API more self-documenting.

For type definitions, extend existing types rather than duplicating their structure. Use intersection types (&) or interface extension to build upon established patterns, ensuring consistency and reducing maintenance overhead.

Example of good parameter design:
```typescript
// Instead of multiple boolean parameters:
function query(clientID: string, query: Query, enabled: boolean, requireComplete: boolean)

// Use an options object:
function query(clientID: string, query: Query, options: {
  enabled?: boolean;
  requireComplete?: boolean;
})
```

Example of good type composition:
```typescript
// Instead of duplicating structure:
export type UseSuspenseQueryOptions = {
  ttl?: TTL | undefined;
  suspendUntil?: 'complete' | 'non-empty';
};

// Extend existing types:
export type UseSuspenseQueryOptions = UseQueryOptions & {
  suspendUntil?: 'complete' | 'non-empty';
};
```

This approach makes APIs more maintainable, self-documenting, and easier to extend without breaking changes.