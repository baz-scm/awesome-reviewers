---
title: Use consistent error types
description: Always use the appropriate error classes and throwing mechanisms for
  consistent error handling across the codebase. Prefer `BetterAuthError` or `APIError`
  over generic `Error` classes, use `throw` instead of returning error responses in
  endpoints, and structure error codes consistently.
repository: better-auth/better-auth
label: Error Handling
language: TypeScript
comments_count: 6
repository_stars: 19651
---

Always use the appropriate error classes and throwing mechanisms for consistent error handling across the codebase. Prefer `BetterAuthError` or `APIError` over generic `Error` classes, use `throw` instead of returning error responses in endpoints, and structure error codes consistently.

Key practices:
- Use `BetterAuthError` instead of `new Error()` for domain-specific errors
- Use `throw ctx.error` or `throw new APIError` in endpoints instead of `return ctx.json(error)`
- Use `toThrowError` with specific error details in tests instead of generic `toThrow()`
- Structure error codes consistently using ERROR_CODES constants
- Use appropriate HTTP status codes (e.g., `BAD_REQUEST` instead of `USER_NOT_FOUND` for client errors)

Example:
```typescript
// ❌ Avoid
throw new Error("unable to set a future iat time");
return ctx.json({ error: "invalid_grant" }, { status: 400 });

// ✅ Prefer  
throw new BetterAuthError("unable to set a future iat time");
throw new APIError("BAD_REQUEST", {
  message: ERROR_CODES.INVALID_GRANT,
  code: "INVALID_GRANT"
});
```

This ensures proper error type inference, consistent error handling patterns, and better debugging experience across the application.