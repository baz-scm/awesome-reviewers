---
title: Consistent database naming
description: 'Maintain consistent naming patterns across all database objects. Ensure
  that:


  1. Related object names are aligned (e.g., indexes should reference their table
  names)'
repository: langfuse/langfuse
label: Naming Conventions
language: Sql
comments_count: 3
repository_stars: 13574
---

Maintain consistent naming patterns across all database objects. Ensure that:

1. Related object names are aligned (e.g., indexes should reference their table names)
2. All identifiers follow the same formatting style (e.g., if using backticks for column names, apply them to all columns)
3. Data type names are spelled correctly and consistently

Example of good practice:
```sql
CREATE TABLE "default_llm_models" (
    "id" TEXT NOT NULL,
    "project_id" TEXT NOT NULL,
    -- other columns...
);

-- Index name matches table name
CREATE INDEX "default_llm_models_project_id_id_key" ON "default_llm_models"("project_id", "id");
```

Example of consistent column formatting:
```sql
CREATE TABLE blob_storage_file_log
(
    `id` String,
    `project_id` String,
    -- All columns use consistent backtick formatting
    `event_ts` DateTime64(3),
    `is_deleted` UInt8
);
```

Consistent naming patterns improve readability, reduce errors, and make database schemas more maintainable.