---
title: Validate before usage
description: Always explicitly check for null or undefined values before using them
  in operations. Don't assume values exist - validate their presence and handle missing
  cases appropriately with early returns, error throwing, or fallback logic.
repository: better-auth/better-auth
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 19651
---

Always explicitly check for null or undefined values before using them in operations. Don't assume values exist - validate their presence and handle missing cases appropriately with early returns, error throwing, or fallback logic.

When working with potentially nullable values, implement explicit checks rather than relying on implicit behavior:

```typescript
// ❌ Avoid - assumes value exists
const result = await handleOAuthUserInfo(ctx, {
  userInfo: { email: userInfo.email } // email could be null/undefined
});

// ✅ Good - validate before usage  
if (!userInfo.email) {
  throw new APIError("BAD_REQUEST", {
    message: "Email is required"
  });
}

// ❌ Avoid - proceeding without validation
const key = getIp(req, ctx.options) + path;

// ✅ Good - check and handle missing values
const ip = getIp(req, ctx.options);
if (!ip) {
  return; // Skip rate limiting if IP unavailable
}
const key = ip + path;
```

This prevents runtime errors, makes code behavior predictable, and ensures proper error handling when required values are missing. Consider whether missing values should trigger errors, fallbacks, or early returns based on your application's requirements.