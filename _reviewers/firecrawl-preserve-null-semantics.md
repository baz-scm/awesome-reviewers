---
title: preserve null semantics
description: When null or undefined values represent meaningful absence of data, preserve
  them rather than converting to default values like empty strings, arrays, or placeholder
  text. Converting these values can lose semantic meaning and create unnecessary data
  storage or processing overhead.
repository: firecrawl/firecrawl
label: Null Handling
language: TypeScript
comments_count: 2
repository_stars: 54535
---

When null or undefined values represent meaningful absence of data, preserve them rather than converting to default values like empty strings, arrays, or placeholder text. Converting these values can lose semantic meaning and create unnecessary data storage or processing overhead.

For example, prefer null over string literals for unknown enum values:
```typescript
// Avoid - stores unnecessary text in database
export enum IntegrationEnum {
  UNKNOWN = "unknown"
}

// Prefer - null represents true absence
export enum IntegrationEnum {
  // omit unknown case, handle with null checks
}
```

Similarly, when making parameters optional, let undefined flow through rather than converting to defaults:
```typescript
// Avoid - loses the semantic difference between undefined and empty
let jsonData = { urls: urls || [], ...params };

// Prefer - preserves undefined semantics
let jsonData = { urls, ...params };
```

This approach maintains clearer data contracts and prevents ambiguity between "no data provided" and "empty data provided".