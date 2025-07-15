---
title: Ensure deterministic query results
description: Always ensure database queries produce deterministic results by including
  explicit ORDER BY clauses when using LIMIT operations. This prevents unpredictable
  result ordering and potential data inconsistencies.
repository: langfuse/langfuse
label: Database
language: TypeScript
comments_count: 5
repository_stars: 13574
---

Always ensure database queries produce deterministic results by including explicit ORDER BY clauses when using LIMIT operations. This prevents unpredictable result ordering and potential data inconsistencies.

Key practices:
1. Include ORDER BY with meaningful columns for result ordering
2. Document any assumptions about result ordering
3. Consider performance implications of ordering choices

Example:
```sql
-- Incorrect: Non-deterministic ordering
SELECT * 
FROM traces
WHERE project_id = ${projectId}
LIMIT 1;

-- Correct: Deterministic ordering
SELECT * 
FROM traces
WHERE project_id = ${projectId}
ORDER BY event_ts DESC, id
LIMIT 1;
```

This practice is especially important when:
- Paginating results
- Selecting latest/newest records
- Using LIMIT with GROUP BY
- Implementing skip indexes