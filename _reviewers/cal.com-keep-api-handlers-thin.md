---
title: Keep API handlers thin
description: API handlers should be lightweight and focused on request/response handling,
  not business logic. Extract specific parameters from requests and delegate complex
  operations to dedicated services rather than handling everything in the controller.
repository: calcom/cal.com
label: API
language: TypeScript
comments_count: 3
repository_stars: 37732
---

API handlers should be lightweight and focused on request/response handling, not business logic. Extract specific parameters from requests and delegate complex operations to dedicated services rather than handling everything in the controller.

Key principles:
- Parse and extract only the specific data needed from requests
- Avoid passing entire request objects to service methods
- Delegate business logic to application services
- Keep handlers focused on HTTP concerns (parsing, validation, response formatting)

Example of what to avoid:
```typescript
async reassignBooking(bookingUid: string, requestUser: UserWithProfile, request: Request) {
  // Handler doing too much work with entire request object
}
```

Better approach:
```typescript
async reassignBooking(bookingUid: string, requestUser: UserWithProfile, teamMemberEmail?: string) {
  // Extract specific parameter in handler, pass only what's needed
  const teamMemberEmail = req.query.teamMemberEmail;
  return this.bookingService.reassignBooking(bookingUid, requestUser, teamMemberEmail);
}
```

This pattern improves testability, reduces coupling, and makes the API surface clearer by explicitly showing what data each operation requires.