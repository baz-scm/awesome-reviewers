---
title: Use transactions for consistency
description: Always wrap multiple related database operations in a transaction to
  ensure data consistency and prevent partial updates. This applies to operations
  across different tables or when coordinating database updates with external services
  (e.g., Redis cache).
repository: elie222/inbox-zero
label: Database
language: TypeScript
comments_count: 9
repository_stars: 8267
---

Always wrap multiple related database operations in a transaction to ensure data consistency and prevent partial updates. This applies to operations across different tables or when coordinating database updates with external services (e.g., Redis cache).

Example:
```diff
- const dbPromise = prisma.label.upsert({ ... })
- const redisPromise = saveUserLabel({ ... })
- await Promise.all([dbPromise, redisPromise])

+ await prisma.$transaction(async (tx) => {
+   const dbResult = await tx.label.upsert({ ... });
+   await saveUserLabel({ ... });
+ });
```

Key benefits:
- Ensures all operations succeed or fail together
- Prevents inconsistent state between related data
- Maintains referential integrity
- Simplifies error handling and rollbacks

Apply this pattern when:
- Updating multiple related records
- Coordinating DB changes with cache updates
- Performing data migrations or merges
- Managing cross-service data consistency