---
title: Avoid nested ternaries
description: Avoid using nested ternary operators as they significantly reduce code
  readability and make debugging difficult. Complex conditional logic should be refactored
  into clear, readable structures using if-else statements, early returns, or extracted
  helper functions.
repository: calcom/cal.com
label: Code Style
language: TypeScript
comments_count: 3
repository_stars: 37732
---

Avoid using nested ternary operators as they significantly reduce code readability and make debugging difficult. Complex conditional logic should be refactored into clear, readable structures using if-else statements, early returns, or extracted helper functions.

**Why this matters:**
- Nested ternaries create cognitive overhead and are hard to parse
- They become "a nightmare to debug" when logic gets complex
- Code readability is crucial for maintainability and team collaboration

**How to refactor:**

Instead of nested ternaries like this:
```typescript
slotStartTime = slotStartTime.minute() % interval !== 0
  ? showOptimizedSlots
    ? rangeEnd.diff(slotStartTime, "minutes") % interval > interval - slotStartTime.minute()
      ? slotStartTime.add(interval - slotStartTime.minute(), "minute")
      : slotStartTime.add(rangeEnd.diff(slotStartTime, "minutes") % interval, "minute")
    : slotStartTime.startOf("hour").add(Math.ceil(slotStartTime.minute() / interval) * interval, "minute")
  : slotStartTime;
```

Refactor to clear conditional blocks:
```typescript
if (slotStartTime.minute() % interval === 0) {
  // No adjustment needed
  return slotStartTime;
}

if (showOptimizedSlots) {
  const timeDiff = rangeEnd.diff(slotStartTime, "minutes") % interval;
  const minutesToAdd = timeDiff > interval - slotStartTime.minute() 
    ? interval - slotStartTime.minute()
    : timeDiff;
  return slotStartTime.add(minutesToAdd, "minute");
}

return slotStartTime
  .startOf("hour")
  .add(Math.ceil(slotStartTime.minute() / interval) * interval, "minute");
```

**Additional guidelines:**
- Use early returns to reduce nesting levels
- Extract complex conditions into well-named boolean variables
- Consider breaking complex logic into smaller, focused functions
- Add comments to explain the business logic when conditions are complex