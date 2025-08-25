---
title: Centralize workflow scheduling
description: Avoid scattering workflow scheduling logic across multiple handlers.
  Instead, create dedicated service methods for different workflow contexts to improve
  maintainability and reduce duplication.
repository: calcom/cal.com
label: Temporal
language: TypeScript
comments_count: 2
repository_stars: 37732
---

Avoid scattering workflow scheduling logic across multiple handlers. Instead, create dedicated service methods for different workflow contexts to improve maintainability and reduce duplication.

When workflow scheduling logic becomes scattered across handlers, it leads to code duplication and makes the system harder to maintain. The solution is to centralize this logic in a dedicated WorkflowService with context-specific methods.

**Problem:** Multiple calls to `scheduleWorkflowReminders` scattered throughout handlers, with complex filtering logic duplicated across different files.

**Solution:** Create dedicated service methods for each workflow context:

```typescript
// Instead of scattered calls across handlers
await scheduleWorkflowReminders({ evt, workflows: filteredWorkflows, ... });

// Use dedicated service methods
await WorkflowService.scheduleWorkflowsOnNewBooking({ 
  evt, 
  isFirstBooking, 
  isPaid, 
  ... 
});

await WorkflowService.scheduleWorkflowsOnConfirmation({ 
  evt, 
  isFirstBooking, 
  isPaid, 
  ... 
});
```

This approach encapsulates workflow orchestration logic, reduces duplication, and makes the codebase more maintainable by providing clear entry points for different workflow scenarios.