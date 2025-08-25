---
title: Design contextual API interfaces
description: API interfaces should expose only relevant data and functionality based
  on context, configuration, and user requirements. This principle ensures efficient
  data transfer, cleaner interfaces, and appropriate user experiences.
repository: calcom/cal.com
label: API
language: TSX
comments_count: 5
repository_stars: 37732
---

API interfaces should expose only relevant data and functionality based on context, configuration, and user requirements. This principle ensures efficient data transfer, cleaner interfaces, and appropriate user experiences.

Key practices:
- Pass only required fields instead of entire objects to minimize data transfer
- Filter available actions/responses based on entity configuration flags
- Adapt interface behavior for different contexts (e.g., different app types, user permissions)
- Remove unnecessary parameters from API calls
- Use generic, context-appropriate naming for API events and methods

Example from the discussions:
```typescript
// Instead of passing the entire schedule object
const DeleteDialogButton = ({ schedule, ... }) => {
  // Only pass required fields
  const DeleteDialogButton = ({ scheduleId, scheduleName, ... }) => {

// Filter actions based on configuration
const isDisabledCancelling = booking.eventType.disableCancelling;
const isDisabledRescheduling = booking.eventType.disableRescheduling;

if (isDisabledCancelling) {
  bookedActions = bookedActions.filter((action) => action.id !== "cancel");
}

if (isDisabledRescheduling) {
  bookedActions.forEach((action) => {
    if (action.id === "edit_booking") {
      action.actions = action.actions?.filter(
        ({ id }) => id !== "reschedule" && id !== "reschedule_request"
      );
    }
  });
}
```

This approach reduces payload sizes, improves performance, and creates more maintainable API contracts that clearly communicate their requirements and capabilities.