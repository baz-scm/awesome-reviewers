---
title: Use semantic null handling
description: When designing APIs and data structures, be intentional about null and
  undefined usage. Use null and undefined with distinct semantic meanings rather than
  interchangeably. For example, undefined can indicate "not yet loaded" while null
  indicates "does not exist". However, avoid nullable types when simpler alternatives
  serve the same purpose - if an empty...
repository: mastodon/mastodon
label: Null Handling
language: TypeScript
comments_count: 2
repository_stars: 48691
---

When designing APIs and data structures, be intentional about null and undefined usage. Use null and undefined with distinct semantic meanings rather than interchangeably. For example, undefined can indicate "not yet loaded" while null indicates "does not exist". However, avoid nullable types when simpler alternatives serve the same purpose - if an empty string conveys the same meaning as null (like "no description available"), prefer the empty string to simplify type handling.

Example of meaningful null/undefined distinction:
```typescript
// Good: Semantic distinction
function useAccountId() {
  // undefined = not fetched yet, null = doesn't exist
  if (accountId) {
    return accountId;
  }
  return undefined; // or null, depending on semantic meaning
}
```

Example of avoiding unnecessary nullables:
```typescript
// Instead of: avatar_description: string | null
// Prefer: avatar_description: string (empty string when no description)
interface AccountShape {
  avatar_description: string; // "" means no description
  header_description: string; // "" means no description
}
```