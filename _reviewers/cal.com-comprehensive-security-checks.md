---
title: comprehensive security checks
description: Ensure that security checks for authorization, authentication, and information
  disclosure are comprehensive and consistently applied across all contexts, rather
  than being conditional on specific scenarios or implementation details.
repository: calcom/cal.com
label: Security
language: TSX
comments_count: 3
repository_stars: 37732
---

Ensure that security checks for authorization, authentication, and information disclosure are comprehensive and consistently applied across all contexts, rather than being conditional on specific scenarios or implementation details.

Security measures should not be limited by contextual conditions. For example, don't restrict admin/owner permission checks to only team event types - apply them universally. Similarly, ensure that redirects and URL handling don't inadvertently expose sensitive information like private booking paths.

Example of comprehensive authorization:
```typescript
// Instead of conditional checks:
if (eventType.teamId) {
  const hasTeamOrOrgPermissions = await checkTeamOrOrgPermissions(userId, eventType.teamId);
}

// Apply comprehensive checks regardless of context:
const hasTeamOrOrgPermissions = await checkTeamOrOrgPermissions(
  userId, 
  eventType.teamId, 
  eventType.team?.parent?.id
);
```

This approach prevents security gaps that can occur when authorization logic is incomplete or when sensitive information is exposed through inadequate URL handling or redirect mechanisms.