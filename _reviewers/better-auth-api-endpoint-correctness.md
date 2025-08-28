---
title: API endpoint correctness
description: API endpoints must behave according to their intended design, properly
  handling special values and executing expected operations like validation. This
  includes preserving meaningful null values (e.g., null representing "no limit")
  rather than replacing them with default values that change the intended behavior,
  and ensuring validation runs when expected.
repository: better-auth/better-auth
label: API
language: Markdown
comments_count: 2
repository_stars: 19651
---

API endpoints must behave according to their intended design, properly handling special values and executing expected operations like validation. This includes preserving meaningful null values (e.g., null representing "no limit") rather than replacing them with default values that change the intended behavior, and ensuring validation runs when expected.

For example, when creating API keys where `remaining: null` signifies unlimited usage, the endpoint should preserve this null value rather than defaulting to a capped value. Similarly, validation endpoints like `isUsernameAvailable` should actually execute validation logic rather than bypassing it.

```javascript
// Good: Preserve meaningful null values
const apiKey = {
  remaining: null // Correctly represents "no cap"
};

// Bad: Replace null with default that changes behavior  
const apiKey = {
  remaining: remaining || defaultLimit // Unintentionally caps usage
};
```