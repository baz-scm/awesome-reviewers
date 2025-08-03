---
title: Verify authentication logic
description: Ensure authentication validation logic follows expected semantics and
  intuitive implementation. Authentication checks should correctly interpret the presence
  or absence of security tokens, with clear and accurate logging that reflects the
  actual security state.
repository: appwrite/appwrite
label: Security
language: JavaScript
comments_count: 1
repository_stars: 51959
---

Ensure authentication validation logic follows expected semantics and intuitive implementation. Authentication checks should correctly interpret the presence or absence of security tokens, with clear and accurate logging that reflects the actual security state.

When implementing JWT or other token-based authentication:
- Presence of valid tokens should indicate authenticated/valid states
- Absence of tokens should indicate unauthenticated/invalid states
- Log messages and condition branches should match these intuitive expectations

**Example:**
```javascript
// Correct implementation
if (context.req.headers['x-appwrite-user-jwt']) {
  context.log('jwt-is-valid');
  // Proceed with authenticated operations
} else {
  context.log('jwt-is-invalid');
  // Handle unauthenticated state
}
```

This prevents security vulnerabilities that could arise from misinterpreting authentication states and ensures proper access control throughout the application.