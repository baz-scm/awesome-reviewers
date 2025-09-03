---
title: Optimize database queries
description: Structure database queries and schemas for optimal performance by avoiding
  nullable fields when possible, organizing query conditions efficiently, and using
  targeted indexes.
repository: novuhq/novu
label: Database
language: TypeScript
comments_count: 3
repository_stars: 37700
---

Structure database queries and schemas for optimal performance by avoiding nullable fields when possible, organizing query conditions efficiently, and using targeted indexes.

**Key practices:**

1. **Avoid nullable fields for performance**: Use default values instead of nullable fields, especially in ClickHouse where non-null values perform better:
```typescript
// Preferred
severity: { type: CHLowCardinality(CHString('none')) }
critical: { type: CHBoolean(false) }

// Instead of
severity: { type: CHNullable(CHString()) }
critical: { type: CHNullable(CHBoolean()) }
```

2. **Structure conditions to minimize OR operations**: Group related conditions into arrays rather than chaining multiple OR statements:
```typescript
// Preferred - cleaner and more performant
const snoozedCondition: Array<MessageQuery> = [];
if (query.snoozed === false) {
  snoozedCondition.push({ snoozedUntil: { $exists: false } }, { snoozedUntil: null });
}

// Instead of multiple OR statements in the main query
requestQuery.$or = [{ snoozedUntil: { $exists: false } }, { snoozedUntil: null }];
```

3. **Use partial indexes for filtered queries**: Apply partial filter expressions to create more efficient indexes for specific use cases:
```typescript
// Targeted index with partial filtering
messageSchema.index(
  {
    _subscriberId: 1,
    _environmentId: 1,
    read: 1,
    archived: 1,
    seen: 1,
    createdAt: -1,
  },
  {
    name: 'in_app_messages_count',
    partialFilterExpression: { channel: 'in_app' },
  }
);
```

This approach improves query performance, reduces index size, and ensures better database resource utilization across different database systems.