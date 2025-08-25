---
title: Authorization hierarchy verification
description: Always implement comprehensive authorization checks that verify user
  permissions at the appropriate hierarchy level (individual → team → organization)
  before allowing operations. Consider multiple permission levels and provide proper
  fallbacks when users have different roles across teams or organizations.
repository: calcom/cal.com
label: Security
language: TypeScript
comments_count: 9
repository_stars: 37732
---

Always implement comprehensive authorization checks that verify user permissions at the appropriate hierarchy level (individual → team → organization) before allowing operations. Consider multiple permission levels and provide proper fallbacks when users have different roles across teams or organizations.

Key principles:
- Check individual ownership first (userId matches)
- Verify team-level permissions (admin/owner roles) for team resources
- Include organization-level permissions when applicable
- Use Permission-Based Access Control (PBAC) with role-based fallbacks
- Ensure permission dependencies are met (e.g., list permissions before modify permissions)

Example implementation:
```typescript
// Check individual ownership first
const userReschedulingIsOwner = isUserReschedulingOwner(userId, originalRescheduledBooking?.userId);

// Check team-level permissions
let isTeamOwnerOrAdmin = false;
if (isTeamEventType && originalRescheduledBooking?.eventType?.teamId) {
  const membership = await prisma.membership.findFirst({
    where: {
      teamId: originalRescheduledBooking.eventType.teamId,
      userId: user?.id,
      role: { in: [MembershipRole.OWNER, MembershipRole.ADMIN] }
    }
  });
  isTeamOwnerOrAdmin = !!membership;
}

// Check organization-level permissions
const hasOrgPermission = await permissionCheckService.checkPermission({
  userId,
  teamId,
  permission: "organization.adminApi",
  fallbackRoles: [MembershipRole.OWNER, MembershipRole.ADMIN]
});

if (!userReschedulingIsOwner && !isTeamOwnerOrAdmin && !hasOrgPermission) {
  throw new TRPCError({ code: "FORBIDDEN", message: "Insufficient permissions" });
}
```

This prevents unauthorized access by ensuring users can only perform operations they have legitimate permissions for, whether through direct ownership, team membership, or organizational authority.