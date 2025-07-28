---
title: Use safe type guards
description: When implementing type guards for nullable or unknown types, use the
  `in` operator and property existence checks instead of type casting. This approach
  provides better null safety by verifying that properties exist before accessing
  them, preventing runtime errors from null or undefined values.
repository: mastodon/mastodon
label: Null Handling
language: TSX
comments_count: 3
repository_stars: 48691
---

When implementing type guards for nullable or unknown types, use the `in` operator and property existence checks instead of type casting. This approach provides better null safety by verifying that properties exist before accessing them, preventing runtime errors from null or undefined values.

Build layered type guards that check for basic validity first, then use the `in` operator to verify specific properties exist. This creates a chain of safety checks that handles null, undefined, and missing property cases gracefully.

Example:
```typescript
// Instead of unsafe type casting:
const isMenuItem = (item: unknown): item is MenuItem => {
  return !!(item as MenuItem)?.text;
};

// Use safe property checks:
const isMenuItem = (item: unknown): item is MenuItem => {
  if (item === null) {
    return true;
  }
  return typeof item === 'object' && 'text' in item;
};

// Build on existing guards for complex types:
const isActionItem = (item: unknown): item is ActionMenuItem => {
  if (!item || !isMenuItem(item)) {
    return false;
  }
  return 'action' in item;
};
```

This pattern ensures that you never attempt to access properties on null or undefined values, and TypeScript can properly narrow the types based on your checks.