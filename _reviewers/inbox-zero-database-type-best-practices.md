---
title: Database type best practices
description: Select appropriate data types and defaults for database columns to ensure
  data integrity and simplify application code. For timestamp columns, use timezone-aware
  types (TIMESTAMPTZ) when working across different timezones or with UTC offsets.
  For ID columns, configure auto-generation at the database level using functions
  like gen_random_uuid() rather than...
repository: elie222/inbox-zero
label: Database
language: Sql
comments_count: 3
repository_stars: 8267
---

Select appropriate data types and defaults for database columns to ensure data integrity and simplify application code. For timestamp columns, use timezone-aware types (TIMESTAMPTZ) when working across different timezones or with UTC offsets. For ID columns, configure auto-generation at the database level using functions like gen_random_uuid() rather than relying on application code to generate identifiers.

```sql
CREATE TABLE "Entity" (
  -- Auto-generated UUID for primary key
  "id" TEXT NOT NULL DEFAULT gen_random_uuid(),
  -- Timezone-aware timestamps for accurate time handling
  "createdAt" TIMESTAMPTZ(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updatedAt" TIMESTAMPTZ(3) NOT NULL,
  -- Other columns
  "name" TEXT NOT NULL,
  -- JSON for flexible structured data
  "metadata" JSONB
);
```

This approach reduces bugs related to timezone confusion, simplifies code by delegating ID generation to the database, and ensures consistent handling of data types across the application.