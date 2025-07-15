---
title: Use comprehensive JSDoc
description: 'Always use JSDoc format (`/** */`) instead of regular comments (`//`)
  for documenting classes, functions, and interfaces. Documentation should be comprehensive,
  including:'
repository: langchain-ai/langchainjs
label: Documentation
language: TypeScript
comments_count: 7
repository_stars: 15004
---

Always use JSDoc format (`/** */`) instead of regular comments (`//`) for documenting classes, functions, and interfaces. Documentation should be comprehensive, including:

1. Clear purpose descriptions
2. Usage examples where appropriate
3. Proper tags like `@internal` for non-public API elements
4. Cross-references using `{@link ...}` syntax
5. Migration paths for deprecated features

This ensures that documentation integrates correctly with API reference generators and provides developers with sufficient context.

**Example - Before:**
```typescript
// this class uses your clientId, clientSecret and redirectUri
// to get access token and refresh token, if you already have them,
// you can use AuthFlowToken or AuthFlowRefresh instead
export class AuthFlow {
  // ...
}
```

**Example - After:**
```typescript
/**
 * Authentication flow for obtaining access and refresh tokens using clientId,
 * clientSecret and redirectUri.
 * 
 * @example
 * const auth = new AuthFlow({
 *   clientId: process.env.CLIENT_ID,
 *   clientSecret: process.env.CLIENT_SECRET,
 *   redirectUri: "http://localhost:3000/callback"
 * });
 * const tokens = await auth.getTokens();
 * 
 * @see If you already have tokens, consider using {@link AuthFlowToken} or
 * {@link AuthFlowRefresh} instead.
 */
export class AuthFlow {
  // ...
}
```
