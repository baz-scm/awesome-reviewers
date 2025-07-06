---
title: Minimize database joins
description: Prefer direct filtering or specialized service methods over complex JOIN
  operations, especially when maintaining or refactoring database access patterns.
  JOINs across multiple tables can impact performance and make code more difficult
  to maintain, particularly during architectural migrations.
repository: grafana/grafana
label: Database
language: Go
comments_count: 4
repository_stars: 68825
---

Prefer direct filtering or specialized service methods over complex JOIN operations, especially when maintaining or refactoring database access patterns. JOINs across multiple tables can impact performance and make code more difficult to maintain, particularly during architectural migrations.

When possible:
1. Use service methods that perform targeted queries rather than broad data retrieval with post-filtering
2. Filter directly on the primary table using indexed columns
3. Consider database abstraction boundaries when designing queries

For example, instead of:
```sql
-- Complex join approach
SELECT le.* FROM library_element le 
LEFT JOIN folder f ON le.folder_uid = f.uid AND le.org_id = f.org_id
WHERE f.title LIKE '%search_term%'
```

Consider:
```go
// Using specialized service methods
folderUIDs, err := folderService.SearchFolders(c, searchQuery) 
// Then directly filter using the results
builder.Write("WHERE le.folder_uid IN (?)", folderUIDs)
```

When handling cross-database compatibility, remember that complex operations like multi-column `WHERE NOT IN` statements are database-specific extensions. Structure your queries to maintain compatibility or implement database-specific code paths with proper fallbacks.