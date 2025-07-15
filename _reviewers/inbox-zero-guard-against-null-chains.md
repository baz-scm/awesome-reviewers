---
title: Guard against null chains
description: Prevent null pointer exceptions by validating object chains before accessing
  nested properties. Use early returns with null checks instead of optional chaining
  when the rest of the function depends on a non-null value.
repository: elie222/inbox-zero
label: Null Handling
language: TypeScript
comments_count: 3
repository_stars: 8267
---

Prevent null pointer exceptions by validating object chains before accessing nested properties. Use early returns with null checks instead of optional chaining when the rest of the function depends on a non-null value.

Example of problematic code:
```typescript
const messages = user.account.access_token
  ? await getMessagesBatch(messageIds, user.account.access_token)
  : [];
```

Better approach:
```typescript
const accessToken = user.account?.access_token;
if (!accessToken) {
  logger.warn("No access token available");
  return [];
}
const messages = await getMessagesBatch(messageIds, accessToken);
```

Key practices:
1. Extract nested values early with optional chaining
2. Validate critical values before proceeding
3. Use early returns to handle null cases
4. Add logging for null cases to aid debugging
5. Consider using nullish coalescing (??) for providing default values

This pattern improves code reliability by catching null cases early and explicitly, rather than letting them propagate through the codebase.