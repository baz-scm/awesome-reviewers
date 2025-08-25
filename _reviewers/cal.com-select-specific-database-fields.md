---
title: Select specific database fields
description: Always explicitly select only the database fields you actually need instead
  of using broad includes or fetching entire objects. This practice significantly
  improves query performance, reduces memory usage, and minimizes data exposure.
repository: calcom/cal.com
label: Database
language: TypeScript
comments_count: 6
repository_stars: 37732
---

Always explicitly select only the database fields you actually need instead of using broad includes or fetching entire objects. This practice significantly improves query performance, reduces memory usage, and minimizes data exposure.

**Why this matters:**
- Reduces database load and network transfer
- Improves application performance 
- Prevents accidental exposure of sensitive data
- Makes code more maintainable by clearly showing data dependencies

**How to apply:**

Instead of fetching everything:
```typescript
// ❌ Avoid - fetches all fields
const booking = await prisma.booking.findUnique({
  where: { uid: bookingUid },
  include: {
    attendees: true,
    user: true,
    eventType: {
      include: {
        owner: true,
      }
    }
  }
});
```

Be specific about what you need:
```typescript
// ✅ Better - select only required fields
const booking = await prisma.booking.findUnique({
  where: { uid: bookingUid },
  include: {
    attendees: {
      select: {
        id: true,
        email: true,
        name: true
      }
    },
    user: {
      select: {
        id: true,
        name: true
      }
    },
    eventType: {
      select: {
        id: true,
        title: true
      }
    }
  }
});
```

**Special considerations:**
- For JSON columns, you cannot use `select` - use `fields: true` or omit entirely
- Avoid redundant queries when data is already available from previous fetches
- Consider conditional subqueries for performance-critical paths (e.g., only fetch attendees for seated events)