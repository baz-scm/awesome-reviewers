---
title: Optimize database queries
description: Avoid inefficient database query patterns by using batch operations and
  appropriate query types. Instead of making multiple individual queries, use batch
  queries with `in` clauses. When you only need counts, use count queries rather than
  fetching full records.
repository: better-auth/better-auth
label: Database
language: TypeScript
comments_count: 2
repository_stars: 19651
---

Avoid inefficient database query patterns by using batch operations and appropriate query types. Instead of making multiple individual queries, use batch queries with `in` clauses. When you only need counts, use count queries rather than fetching full records.

Examples of improvements:
- Replace multiple individual queries with a single batch query:
```typescript
// Instead of multiple queries in a loop
const rolePromises = userRoles.map(async (userRole) => {
  return ctx.context.adapter.findOne({ model: "role", where: [{ field: "id", value: userRole.roleId }] });
});

// Use a single batch query
const roleIds = userRoles.map(ur => ur.roleId);
const roles = await ctx.context.adapter.findMany({ 
  model: "role", 
  where: [{ field: "id", operator: "in", value: roleIds }] 
});
```

- Use count queries when you don't need the actual data:
```typescript
// Instead of fetching all records
const allUsers = await db.findMany({ model: "user" });
const userCount = allUsers.length;

// Use count directly
const userCount = await db.count({ model: "user" });
```

This approach reduces database load, improves response times, and minimizes memory usage by avoiding unnecessary data transfer.