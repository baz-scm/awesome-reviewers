---
title: Auth-Gated Validation
description: 'Apply security controls at the UI/component level and ensure input validation
  is centralized.


  1) Auth-state gating (authorization/flow correctness)

  - Don’t render or enable actions when the user’s authentication state makes them
  invalid. Check auth state at the component boundary.'
repository: kamranahmedse/developer-roadmap
label: Security
language: TSX
comments_count: 2
repository_stars: 354523
---

Apply security controls at the UI/component level and ensure input validation is centralized.

1) Auth-state gating (authorization/flow correctness)
- Don’t render or enable actions when the user’s authentication state makes them invalid. Check auth state at the component boundary.

```tsx
export function SubscribeToChangelog({ isLoggedIn }: { isLoggedIn: boolean }) {
  if (isLoggedIn) return null; // or an alternative message
  return <button onClick={/* show subscribe flow */}>Subscribe</button>;
}
```

2) Centralize validation rules (input validation consistency)
- Avoid duplicating “regex + length” checks across handlers/components. Either:
  - Put constraints into the regex and only call `.test(value)`, or
  - Create a single helper and reuse it everywhere.

```ts
const USERNAME_REGEX = /^[a-zA-Z0-9]{0,20}$/; // includes length constraint
export function isUsernameValid(value: string) {
  return USERNAME_REGEX.test(value);
}

// usage
const isValid = isUsernameValid(value);
```

This prevents unauthorized/incorrect flows from appearing to the user and reduces the risk of inconsistent validation logic across the codebase.