---
title: Use proper authorization attributes
description: Avoid using Django framework attributes like `is_staff` and `is_impersonated`
  for application role checking, as these serve different purposes (admin panel access
  and user impersonation respectively). Instead, use application-specific role validation
  methods to ensure proper authorization.
repository: PostHog/posthog
label: Security
language: TSX
comments_count: 1
repository_stars: 28460
---

Avoid using Django framework attributes like `is_staff` and `is_impersonated` for application role checking, as these serve different purposes (admin panel access and user impersonation respectively). Instead, use application-specific role validation methods to ensure proper authorization.

For role-based access control, import and use the appropriate organization logic:

```typescript
const { isAdminOrOwner } = useValues(organizationLogic)

// Use this instead of user?.is_staff
if (isAdminOrOwner) {
    // Admin/owner specific logic
}
```

This prevents potential authorization bypass vulnerabilities that could occur when framework attributes are misused for application-level access control decisions.