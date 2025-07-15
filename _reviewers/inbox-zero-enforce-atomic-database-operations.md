---
title: Enforce atomic database operations
description: Replace check-then-act patterns with atomic database operations to prevent
  race conditions in concurrent environments. Use transactions for multi-step operations
  and leverage database-level constraints instead of application-level checks.
repository: elie222/inbox-zero
label: Concurrency
language: TypeScript
comments_count: 6
repository_stars: 8267
---

Replace check-then-act patterns with atomic database operations to prevent race conditions in concurrent environments. Use transactions for multi-step operations and leverage database-level constraints instead of application-level checks.

Example - Transform this race-prone code:
```typescript
// DON'T: Check-then-act pattern
const existing = await prisma.newsletter.findUnique({
  where: { email_userId: { email, userId } }
});
if (!existing?.analyzed) {
  await prisma.newsletter.create({
    data: { email, userId, analyzed: true }
  });
}
```

Into atomic operation:
```typescript
// DO: Use upsert for atomic operation
await prisma.newsletter.upsert({
  where: { email_userId: { email, userId } },
  update: { analyzed: true },
  create: { email, userId, analyzed: true }
});

// DO: Use transactions for multi-step operations
await prisma.$transaction(async (tx) => {
  const result = await tx.newsletter.findUnique({/*...*/});
  if (result) {
    await tx.newsletter.update({/*...*/});
  }
});
```

Key practices:
- Use upsert instead of separate find/create
- Wrap related operations in transactions
- Handle unique constraint violations (e.g., Prisma P2002 errors)
- Add database-level constraints rather than relying on application checks
- Consider using advisory locks for complex operations