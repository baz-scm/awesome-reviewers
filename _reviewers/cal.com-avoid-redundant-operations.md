---
title: Avoid redundant operations
description: 'Identify and eliminate duplicate or inefficient operations that waste
  computational resources. Common patterns to watch for include:


  1. **Duplicate function calls**: Multiple calls to expensive operations like database
  queries or API endpoints within the same request flow'
repository: calcom/cal.com
label: Performance Optimization
language: TypeScript
comments_count: 4
repository_stars: 37732
---

Identify and eliminate duplicate or inefficient operations that waste computational resources. Common patterns to watch for include:

1. **Duplicate function calls**: Multiple calls to expensive operations like database queries or API endpoints within the same request flow
2. **Inefficient database queries**: Fetching all records and filtering in memory instead of using proper WHERE clauses
3. **Excessive API calls**: Triggering API calls on frequent user interactions like keystrokes without debouncing

Example of problematic code:
```typescript
// Bad: Duplicate expensive calls
await getAvailableSlots({...}); // calls getUserAvailability internally
await ensureAvailableUsers({...}); // also calls getUserAvailability internally

// Bad: Inefficient database query
const allSubscriptions = await prisma.calendarSubscription.findMany({
  select: { selectedCalendarId: true },
});
const excludeIds = allSubscriptions.map((sub) => sub.selectedCalendarId);

// Good: Single call or proper WHERE clause
await ensureAvailableUsers({users: [...users, ...guests]});

// Good: Efficient database query
const selectedCalendars = await prisma.selectedCalendar.findMany({
  where: { calendarSubscriptionId: null }
});
```

Before implementing functionality, analyze the call flow to identify potential redundant operations and consolidate them into single, efficient calls.