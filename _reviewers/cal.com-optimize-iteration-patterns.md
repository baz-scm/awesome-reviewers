---
title: optimize iteration patterns
description: Minimize computational complexity by optimizing iteration patterns and
  data processing flows. Apply early filtering when possible, but preserve data integrity
  when order or indexing matters.
repository: calcom/cal.com
label: Algorithms
language: TypeScript
comments_count: 4
repository_stars: 37732
---

Minimize computational complexity by optimizing iteration patterns and data processing flows. Apply early filtering when possible, but preserve data integrity when order or indexing matters.

**Key principles:**
1. **Filter early**: Apply filters at the data source rather than after multiple transformations
2. **Avoid nested loops**: Replace nested iterations with more efficient single-pass algorithms when possible
3. **Consider data integrity**: Sometimes separate operations are necessary to maintain correct indexing or ordering

**Examples:**

❌ **Avoid late filtering:**
```typescript
const allWorkflows = eventTypeWorkflows;
// ... multiple operations on allWorkflows
const workflows = allWorkflows.filter((workflow) => {
  if (triggerEvents && !triggerEvents.includes(workflow.trigger)) return false;
});
```

✅ **Filter early:**
```typescript
const allWorkflows = eventTypeWorkflows.filter((workflow) => {
  return !triggerEvents || triggerEvents.includes(workflow.trigger);
});
```

❌ **Avoid nested loops when possible:**
```typescript
for (let i = 0; i < bookingsWithRemainingSeats.length; i++) {
  for (let j = i; j < busyTimes.length; j++) {
    // processing logic
  }
}
```

✅ **Single iteration approach:**
```typescript
bookings.forEach(booking => {
  if (booking.attendeesCount < eventType.seatsPerTimeSlot) {
    // process booking directly
  }
});
```

⚠️ **Exception - preserve data integrity:**
```typescript
// When index position matters, separate filter + reduce is correct
.filter((attendee) => typeof attendee.name === "string" && typeof attendee.email === "string")
.reduce((acc, attendee, index) => {
  acc[`Attendee ${index + 1}`] = `${attendee.name} (${attendee.email})`;
  return acc;
}, {})
```

This approach reduces time complexity from O(n²) to O(n) in many cases while maintaining code correctness.