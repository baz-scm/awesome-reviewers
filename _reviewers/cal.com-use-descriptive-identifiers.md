---
title: Use descriptive identifiers
description: Choose specific, descriptive names for variables, functions, and parameters
  that clearly communicate their purpose and content. Avoid generic terms that could
  be ambiguous or misleading.
repository: calcom/cal.com
label: Naming Conventions
language: TypeScript
comments_count: 5
repository_stars: 37732
---

Choose specific, descriptive names for variables, functions, and parameters that clearly communicate their purpose and content. Avoid generic terms that could be ambiguous or misleading.

**Key principles:**
- Replace generic names with specific, contextual ones
- Ensure names accurately reflect the data or functionality they represent
- Avoid names that could be confused with other similar concepts
- Consider the broader context where the identifier will be used

**Examples of improvements:**
```typescript
// ❌ Generic and potentially misleading
const userInfo = rawBookingData.user;
const users = await prisma.user.findMany({...});
const redirectTo = userId;

// ✅ Specific and descriptive  
const bookingSlug = rawBookingData.user;
const attendeesAvailability = await prisma.user.findMany({...});
const redirectToUserId = userId;
```

**Avoid naming conflicts:**
```typescript
// ❌ Confusing - boolean vs string with same base name
customLabel: true,        // boolean property
customLabel: "My Label"   // string in options

// ✅ Clear distinction
supportsCustomLabel: true,    // boolean property  
customLabel: "My Label"       // string in options
```

This practice improves code readability, reduces cognitive load, and prevents misunderstandings about data types and purposes.