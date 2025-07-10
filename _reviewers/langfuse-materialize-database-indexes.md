---
title: Materialize database indexes
description: Always materialize database indexes after creation to ensure they are
  fully built and immediately available for queries. This is especially important
  in migration scripts where database performance shouldn't be compromised during
  or after the migration process. Without materialization, indexes may not be immediately
  usable, causing potential performance...
repository: langfuse/langfuse
label: Database
language: Sql
comments_count: 2
repository_stars: 13574
---

Always materialize database indexes after creation to ensure they are fully built and immediately available for queries. This is especially important in migration scripts where database performance shouldn't be compromised during or after the migration process. Without materialization, indexes may not be immediately usable, causing potential performance issues until the background materialization completes.

Example in ClickHouse:
```sql
-- Always follow index creation with materialization
ALTER TABLE scores ON CLUSTER default ADD INDEX IF NOT EXISTS idx_project_session (project_id, session_id) TYPE bloom_filter(0.001) GRANULARITY 1;
ALTER TABLE scores ON CLUSTER default MATERIALIZE INDEX IF EXISTS idx_project_session;
```

This two-step approach ensures that indexes are not only created but also immediately available for use in subsequent queries.