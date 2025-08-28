---
title: Prefer simple solutions
description: Choose existing utilities, simpler patterns, and cleaner implementations
  over manual or complex approaches. This improves code maintainability and reduces
  potential bugs.
repository: better-auth/better-auth
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 19651
---

Choose existing utilities, simpler patterns, and cleaner implementations over manual or complex approaches. This improves code maintainability and reduces potential bugs.

Key practices:
- Use built-in utilities instead of manual parsing (e.g., `ctx.getCookie()` instead of manually parsing cookie strings)
- Prefer functions over classes when simple state management suffices
- Remove debug statements like `console.log()` from production code
- Simplify control flow by avoiding unnecessary `else if` chains when independent conditions can be used
- Extract and reuse functions instead of duplicating logic

Example of preferred approach:
```typescript
// Instead of manual parsing:
const cookies = cookieString.split(";").map(cookie => cookie.trim());

// Use existing utility:
const cookieValue = ctx.getCookie(cookieName);

// Instead of else-if chains:
if (authentication === "basic") {
    requestHeaders["authorization"] = `Basic ${encodedCredentials}`;
}
if (authentication !== "basic" && options.clientSecret) {
    body.set("client_secret", options.clientSecret);
}
```

This approach reduces complexity, leverages tested utilities, and makes code more readable and maintainable.