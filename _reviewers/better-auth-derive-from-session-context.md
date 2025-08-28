---
title: derive from session context
description: Always derive sensitive identifiers and permissions from the authenticated
  session context rather than accepting them as user input. This prevents privilege
  escalation attacks where users could manipulate request parameters to access unauthorized
  resources or perform actions on behalf of other users.
repository: better-auth/better-auth
label: Security
language: TypeScript
comments_count: 4
repository_stars: 19651
---

Always derive sensitive identifiers and permissions from the authenticated session context rather than accepting them as user input. This prevents privilege escalation attacks where users could manipulate request parameters to access unauthorized resources or perform actions on behalf of other users.

Instead of accepting sensitive IDs like `stripeCustomerId` or `organizationId` directly from request bodies, retrieve them from the authenticated session or validate that the user has permission to access the specified resource. Use session middleware to automatically reject requests without valid sessions.

Example of vulnerable pattern:
```typescript
// BAD: Trusting user input for sensitive operations
body: z.object({
  stripeCustomerId: z.string(), // User could provide any customer ID
  organizationId: z.string(),   // User could access any organization
})

// GOOD: Derive from session context
const session = await getSessionFromCtx(ctx);
const user = session.user;
const stripeCustomerId = user.stripeCustomerId; // From authenticated user
const organizationId = await getUserOrganization(user.id); // Validated access
```

This approach ensures that all operations are properly scoped to the authenticated user's permissions and prevents unauthorized access to resources belonging to other users.