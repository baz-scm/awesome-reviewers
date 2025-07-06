---
title: Use appropriate permission checks
description: 'When implementing role-based access control (RBAC), ensure you use the
  correct permission verification method based on the security context. Distinguish
  between:'
repository: grafana/grafana
label: Security
language: TSX
comments_count: 1
repository_stars: 68825
---

When implementing role-based access control (RBAC), ensure you use the correct permission verification method based on the security context. Distinguish between:

1. User-level permissions: Use `hasPermission()` when checking if the current user has a specific permission, regardless of the object being accessed.

2. Object-specific permissions: Use `hasPermissionInMetadata()` when verifying if access is allowed for a specific object based on its metadata.

Using the wrong permission check can lead to security vulnerabilities or overly restrictive access. Always confirm which level of permission verification is required for your use case.

Example:
```typescript
// For user-level permission check
if (!contextSrv.hasPermission(AccessControlAction.PluginsWrite)) {
  // Handle unauthorized access
}

// For object-specific permission check
if (!contextSrv.hasPermissionInMetadata(AccessControlAction.PluginsWrite, plugin)) {
  // Handle unauthorized access
}
```