---
title: prefer authentication wrappers
description: Use authentication wrapper functions or higher-order functions that automatically
  handle unauthenticated calls rather than manually checking authentication status.
  These wrappers provide built-in security by ensuring that authentication edge cases
  are handled consistently and reducing the risk of forgetting to validate authentication
  in handlers.
repository: better-auth/better-auth
label: Security
language: Markdown
comments_count: 1
repository_stars: 19651
---

Use authentication wrapper functions or higher-order functions that automatically handle unauthenticated calls rather than manually checking authentication status. These wrappers provide built-in security by ensuring that authentication edge cases are handled consistently and reducing the risk of forgetting to validate authentication in handlers.

For example, prefer using `withMcpAuth` which handles session retrieval and unauthenticated calls automatically:

```javascript
// Preferred: Using authentication wrapper
const handler = withMcpAuth((session, req) => {
  // Handler logic with guaranteed authenticated session
});

// Avoid: Manual authentication checking
const handler = (req) => {
  const session = auth.api.getMcpSession(req);
  // Risk of forgetting to handle null/undefined session
};
```

This approach centralizes authentication logic, reduces code duplication, and minimizes security vulnerabilities from inconsistent authentication handling across your application.