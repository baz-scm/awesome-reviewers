---
title: Validate security configurations
description: Always validate security-related configurations and implementations to
  ensure they follow established security best practices. This includes verifying
  authentication token formats, communication protocols, and error handling mechanisms.
repository: snyk/cli
label: Security
language: TypeScript
comments_count: 3
repository_stars: 5178
---

Always validate security-related configurations and implementations to ensure they follow established security best practices. This includes verifying authentication token formats, communication protocols, and error handling mechanisms.

Key areas to validate:

1. **Authentication tokens**: Use proper Authorization header formats instead of plain tokens. Prefer standard formats like `token <value>` or `bearer <jwt>` over custom implementations.

2. **Communication protocols**: Validate that API URLs use secure HTTPS protocols and warn users when insecure HTTP is detected.

3. **Authentication errors**: Properly handle and propagate authentication failures (401/403 errors) with appropriate error types.

Example implementation:
```typescript
// Validate secure API URL
const apiUrl = config.API_REST_URL;
if (apiUrl.startsWith('http://')) {
  console.warn("You configured the Snyk CLI to use an API URL with an HTTP scheme. This option is insecure and might prevent the Snyk CLI from working correctly.");
}

// Use proper authentication header format
const sessionToken = getAuthHeader(); // Returns "token <value>" format

// Handle authentication errors properly
try {
  return await makeAuthenticatedRequest();
} catch (error) {
  const unauthorized = error.code === 401 || error.code === 403;
  if (unauthorized) {
    throw AuthFailedError(error.error, error.code);
  }
}
```

This validation approach prevents security vulnerabilities by catching misconfigurations early and ensuring consistent security practices across the codebase.