---
title: Configuration access patterns
description: Ensure configuration data is accessed through proper service layers with
  dependency injection rather than direct database calls in presentation components.
  Configuration settings should be retrieved via dedicated repository classes or service
  methods, not through direct Prisma interactions in getServerSideProps or component
  logic.
repository: calcom/cal.com
label: Configurations
language: TSX
comments_count: 4
repository_stars: 37732
---

Ensure configuration data is accessed through proper service layers with dependency injection rather than direct database calls in presentation components. Configuration settings should be retrieved via dedicated repository classes or service methods, not through direct Prisma interactions in getServerSideProps or component logic.

This pattern improves testability, maintainability, and follows proper separation of concerns. Configuration access should be abstracted behind service interfaces that can be easily mocked and tested.

Example of what to avoid:
```typescript
// Bad: Direct Prisma call in getServerSideProps
const teamSettings = await prisma.team.findUnique({
  where: { id: teamId },
  select: {
    mandatoryCancellationReasonForHost: true,
    mandatoryCancellationReasonForAttendee: true,
  },
});
```

Example of proper approach:
```typescript
// Good: Use service layer with dependency injection
const teamSettings = await teamConfigurationService.getTeamCancellationSettings(teamId);
```

Additionally, avoid hardcoded configuration values like `!true` and instead use proper boolean constants or configuration objects that clearly express intent and can be easily modified.