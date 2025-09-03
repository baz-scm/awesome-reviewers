---
title: optimize frequent operations
description: Identify code paths that execute frequently and ensure they use performant,
  non-blocking solutions. Frequent operations should avoid expensive database queries,
  CPU-intensive synchronous processing, or anything that can block the event loop.
repository: firecrawl/firecrawl
label: Performance Optimization
language: TypeScript
comments_count: 2
repository_stars: 54535
---

Identify code paths that execute frequently and ensure they use performant, non-blocking solutions. Frequent operations should avoid expensive database queries, CPU-intensive synchronous processing, or anything that can block the event loop.

For high-frequency database operations, use caching solutions like Redis instead of direct database queries. For CPU-intensive tasks like HTML parsing that run often, consider moving the logic to more performant runtimes or libraries.

Example of what to avoid:
```typescript
// Bad: DB query on every job insert
const { data: recentNotifications } = await supabase_service
  .from("user_notifications")
  .select("*")
  .eq("team_id", team_id)
  .gte("sent_date", pastDate.toISOString());
```

Example of better approach:
```typescript
// Good: Use Redis for frequent lookups
const recentNotifications = await redis.get(`notifications:${team_id}`);
```

Before implementing any operation that will run frequently, evaluate its performance impact and consider alternatives like caching, background processing, or more efficient libraries/runtimes.