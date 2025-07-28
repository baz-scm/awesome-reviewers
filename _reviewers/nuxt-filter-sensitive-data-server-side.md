---
title: Filter sensitive data server-side
description: Always filter sensitive data at the API/server level before sending responses
  to the client. Never rely on client-side filtering or assume that data not displayed
  in the UI is secure. Any data sent to the client should be considered public and
  accessible to anyone with malicious intent.
repository: nuxt/nuxt
label: Security
language: Markdown
comments_count: 2
repository_stars: 57769
---

Always filter sensitive data at the API/server level before sending responses to the client. Never rely on client-side filtering or assume that data not displayed in the UI is secure. Any data sent to the client should be considered public and accessible to anyone with malicious intent.

Key principles:
- APIs should only return the specific fields that the client needs
- Use server-side data transformation to exclude sensitive fields like passwords, internal IDs, or private user information
- Avoid exposing entire database entities or objects that may contain sensitive fields
- Configuration files accessible to the client (like `app.config`) must never contain secrets or sensitive values

Example of proper server-side filtering:
```ts
// ❌ Bad: Returning entire user entity
export default defineEventHandler(async (event) => {
  const user = await db.query.users.findFirst()
  return user // Contains password, internal fields, etc.
})

// ✅ Good: Return only necessary fields
export default defineEventHandler(async (event) => {
  const user = await db.query.users.findFirst()
  return {
    id: user.id,
    email: user.email,
    name: user.name
    // password and other sensitive fields excluded
  }
})
```

Remember: "An API is and should always be considered as something public and accessible." Even if sensitive data isn't displayed in your UI, it can still be accessed by inspecting network requests or the client bundle.