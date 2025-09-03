---
title: consistent authentication patterns
description: Use standardized authentication decorators consistently across all endpoints
  to ensure proper security coverage and follow the principle of least privilege.
  Always use @RequireAuthentication() as the primary way to protect endpoints, and
  explicitly use @SkipPermissionsCheck() for authenticated routes that don't require
  permission validation.
repository: novuhq/novu
label: Security
language: TypeScript
comments_count: 2
repository_stars: 37700
---

Use standardized authentication decorators consistently across all endpoints to ensure proper security coverage and follow the principle of least privilege. Always use @RequireAuthentication() as the primary way to protect endpoints, and explicitly use @SkipPermissionsCheck() for authenticated routes that don't require permission validation.

This approach prevents accidentally leaving endpoints unprotected and maintains consistency in security patterns. The authentication decorator should automatically apply both user authentication and permission guards, with explicit opt-out for permission checks when not needed.

Example:
```typescript
// Standard protected endpoint (requires auth + permissions)
@RequireAuthentication()
async updateEnvironment() { ... }

// Authenticated but no permission check needed
@RequireAuthentication()
@SkipPermissionsCheck()
async listMyEnvironments() { ... }

// Within the endpoint, check specific permissions for sensitive data
if (user.permissions.includes(PermissionsEnum.API_KEY_READ)) {
  // Return sensitive data like API keys
}
```

This pattern ensures security by default while allowing granular control when needed, reducing the risk of security vulnerabilities from inconsistent authentication handling.