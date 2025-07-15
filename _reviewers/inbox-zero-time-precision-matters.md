---
title: Time precision matters
description: 'When implementing algorithms involving date and time calculations, maintain
  precise control over time components to avoid subtle bugs:


  1. **Reset unwanted time components** - Always explicitly set seconds and milliseconds
  to zero when you only care about hours and minutes'
repository: elie222/inbox-zero
label: Algorithms
language: TypeScript
comments_count: 5
repository_stars: 8267
---

When implementing algorithms involving date and time calculations, maintain precise control over time components to avoid subtle bugs:

1. **Reset unwanted time components** - Always explicitly set seconds and milliseconds to zero when you only care about hours and minutes
2. **Preserve fractional values** in intermediate calculations rather than rounding prematurely
3. **Be consistent** about which time components you manipulate and which you preserve
4. **Consider time boundaries** when comparing dates

```typescript
// ❌ PROBLEMATIC: Implicit time components cause non-deterministic behavior
const targetTime = setHours(setMinutes(now, 0), 11); // Still has seconds/ms from now

// ✅ CORRECT: Explicitly reset all time components you don't want
const targetTime = setMilliseconds(setSeconds(setMinutes(now, 0), 0), 0) |> 
                   (d => setHours(d, 11));

// ❌ PROBLEMATIC: Rounding can collapse distinct slots
const slotDate = addDays(intervalStart, Math.round(i * slotLength));

// ✅ CORRECT: Preserve fractional precision in intermediate calculations
const wholeDays = Math.floor(i * slotLength);
const slotDate = addDays(intervalStart, wholeDays);

// ❌ PROBLEMATIC: Missing boundary check
if (daysOfWeek & nextDayMask) {
  nextDate.setHours(0, 0, 0, 0);
  return nextDate; // Could return a time in the past
}

// ✅ CORRECT: Check time boundaries
if (daysOfWeek & nextDayMask) {
  nextDate.setHours(0, 0, 0, 0);
  if (daysToAdd === 0 && nextDate <= fromDate) {
    daysToAdd++;
    continue; // Skip to next day
  }
  return nextDate;
}
```

Time-related bugs can be subtle and hard to detect. They often manifest only in specific situations (like date boundaries or daylight saving time changes). Implement thorough tests that cover edge cases, and always be explicit about which time components you're manipulating.