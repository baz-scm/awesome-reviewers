---
title: API consistency standards
description: Maintain consistent parameter formats and requirements across all API
  providers and endpoints. When documentation conflicts with implementation, resolve
  discrepancies to ensure alignment. Avoid breaking changes by designing API modifications
  as unions or optional parameters rather than replacing existing structures.
repository: better-auth/better-auth
label: API
language: Other
comments_count: 3
repository_stars: 19651
---

Maintain consistent parameter formats and requirements across all API providers and endpoints. When documentation conflicts with implementation, resolve discrepancies to ensure alignment. Avoid breaking changes by designing API modifications as unions or optional parameters rather than replacing existing structures.

For example, when adding new authentication methods, extend the existing interface rather than replacing it:

```ts
// Instead of breaking change:
const { data } = await authClient.twoFactor.enable({
    verification: { // This breaks existing code
        password: "password"
    }
});

// Use union types for backward compatibility:
const { data } = await authClient.twoFactor.enable({
    password: "password" // Existing format still works
    // OR otp: "123456" // New option available
});
```

Ensure parameter formats match official provider documentation (e.g., Google's `select_account consent` vs `select_account+consent`) and maintain consistency with established patterns across similar providers within the same system.