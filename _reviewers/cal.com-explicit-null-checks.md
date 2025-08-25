---
title: Explicit null checks
description: Always use explicit null and undefined checks instead of relying solely
  on optional chaining, especially when you need predictable boolean results or want
  to prevent null/undefined values from propagating to APIs, URLs, or causing runtime
  errors.
repository: calcom/cal.com
label: Null Handling
language: TSX
comments_count: 5
repository_stars: 37732
---

Always use explicit null and undefined checks instead of relying solely on optional chaining, especially when you need predictable boolean results or want to prevent null/undefined values from propagating to APIs, URLs, or causing runtime errors.

Use explicit checks with logical operators to ensure clean boolean results:
```typescript
// Preferred: explicit check ensures boolean result
const isPlatformUser = redirectUrl && redirectUrl.includes("platform") && redirectUrl.includes("new");

// Avoid: optional chaining can return undefined, making isPlatformUser potentially undefined
const isPlatformUser = redirectUrl?.includes("platform") && redirectUrl?.includes("new");
```

Provide defensive fallbacks for arrays and objects that might be null/undefined:
```typescript
// Safe array access with fallback
const schedule = (atomSchedule.schedule || []).map(avail => ({
  startTime: new Date(avail.startTime),
  endTime: new Date(avail.endTime),
  days: avail.days,
}));

// Prevent undefined values in object spreads
query: {
  slug: ctx.query.user,
  ...(ctx.query.orgRedirection !== undefined && { orgRedirection: ctx.query.orgRedirection }),
}
```

Check for both null and undefined when the distinction matters:
```typescript
// Comprehensive check for functions that don't accept null
if (value !== undefined && value !== null) {
  return decodeURIComponent(value);
}
```

This approach prevents runtime errors, ensures predictable data types, and makes your code's null-handling behavior explicit and intentional.