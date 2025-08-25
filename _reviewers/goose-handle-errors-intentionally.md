---
title: Handle errors intentionally
description: Avoid generic catch-all error handling that masks important failures.
  Instead, be selective about which errors to handle locally versus letting them bubble
  up to higher-level handlers. When you do handle errors locally, implement safe defaults
  and use robust parsing methods.
repository: block/goose
label: Error Handling
language: TypeScript
comments_count: 4
repository_stars: 19037
---

Avoid generic catch-all error handling that masks important failures. Instead, be selective about which errors to handle locally versus letting them bubble up to higher-level handlers. When you do handle errors locally, implement safe defaults and use robust parsing methods.

Key principles:
- Let errors bubble up unless you can meaningfully handle them at the current level
- When handling errors locally, default to the safest behavior (e.g., showing generic warnings instead of assuming no security issues)
- Use safe parsing methods like `safeJsonParse` instead of raw `JSON.parse()`
- Handle specific error conditions (like HTTP 503/529 status codes) with appropriate recovery strategies

Example of intentional error handling:
```typescript
// Bad: Generic catch that hides all errors
try {
  const result = await response.json();
  return result;
} catch (error) {
  return { success: false }; // Masks what actually went wrong
}

// Good: Let parsing errors bubble up, handle specific conditions
const result = await safeJsonParse(response);

// Handle specific recoverable errors
if (response.status === 529 || response.status === 503) {
  // Retry logic for service overload
  return retryRequest();
}

// For security scans, default to safe behavior on failure
try {
  const scanResult = await scanRecipe(recipeConfig);
  setHasSecurityWarnings(scanResult.has_security_warnings);
} catch (error) {
  setHasSecurityWarnings(false); // Safe default, show generic warning
}
```