---
title: Prefer early returns
description: Use early returns and guard clauses instead of nested if-else statements
  to improve code readability and reduce complexity. Apply the fail-fast principle
  by handling edge cases and invalid conditions first, then proceeding with the main
  logic.
repository: calcom/cal.com
label: Code Style
language: TSX
comments_count: 4
repository_stars: 37732
---

Use early returns and guard clauses instead of nested if-else statements to improve code readability and reduce complexity. Apply the fail-fast principle by handling edge cases and invalid conditions first, then proceeding with the main logic.

Benefits:
- Reduces nesting levels making code easier to follow
- Makes the happy path more prominent and readable  
- Eliminates unnecessary else clauses
- Improves maintainability by clearly separating error handling from business logic

Examples:

Instead of:
```javascript
const isCancellationReasonRequired = () => {
  if (!props.teamCancellationSettings) {
    return props.isHost;
  }
  
  if (props.isHost) {
    return props.teamCancellationSettings.mandatoryCancellationReasonForHost;
  } else {
    return props.teamCancellationSettings.mandatoryCancellationReasonForAttendee;
  }
};
```

Prefer:
```javascript
const isCancellationReasonRequired = () => {
  if (!props.teamCancellationSettings) {
    return props.isHost;
  }
  
  if (props.isHost) return props.teamCancellationSettings.mandatoryCancellationReasonForHost;
  
  return props.teamCancellationSettings.mandatoryCancellationReasonForAttendee;
};
```

For conditional rendering, handle the simpler/shorter condition first:
```javascript
// Instead of lengthy if-else blocks
{!schedule?.timeBlocks?.length ? (
  <SimpleComponent />
) : (
  <ComplexComponent />
)}
```