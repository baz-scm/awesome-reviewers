---
title: Enforce user scoping
description: All database queries must include appropriate user scoping to prevent
  unauthorized data access and Insecure Direct Object Reference (IDOR) vulnerabilities.
  Every query should filter results based on the authenticated user's context using
  `emailAccountId`, `userId`, or equivalent identifiers in WHERE clauses.
repository: elie222/inbox-zero
label: Security
language: Other
comments_count: 1
repository_stars: 8267
---

All database queries must include appropriate user scoping to prevent unauthorized data access and Insecure Direct Object Reference (IDOR) vulnerabilities. Every query should filter results based on the authenticated user's context using `emailAccountId`, `userId`, or equivalent identifiers in WHERE clauses.

**Why it matters:** Without proper user scoping, attackers could potentially access or modify data belonging to other users by manipulating input parameters or request data.

**Implementation:**

```typescript
// ❌ VULNERABLE: Missing user scoping
const schedule = await prisma.schedule.findUnique({
  where: { id: scheduleId }
});

// ✅ SECURE: Properly scoped to authenticated user
const schedule = await prisma.schedule.findUnique({
  where: { id: scheduleId, emailAccountId }
});
```

**Security checks:**
- Run security audit scripts regularly to identify unscoped queries
- When reviewing code, always verify that database queries include user context filters
- For relations, ensure that lookups verify ownership through proper joins or nested where clauses
- Be especially vigilant with `findUnique`, `findFirst`, and any query that returns specific records