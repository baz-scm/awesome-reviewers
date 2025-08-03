---
title: Optimize large field queries
description: When working with database queries that process large text fields or
  arrays, choose operations that minimize data conversion and processing overhead.
  This can lead to dramatic performance improvements.
repository: supabase/supabase
label: Performance Optimization
language: TypeScript
comments_count: 2
repository_stars: 86070
---

When working with database queries that process large text fields or arrays, choose operations that minimize data conversion and processing overhead. This can lead to dramatic performance improvements.

For checking text length in PostgreSQL queries, use `octet_length()` instead of `length()` when dealing with large fields:

```sql
-- Less efficient (could be 100x slower for large fields)
when length(field_name::text) > 10240 then ...

-- More efficient
when octet_length(field_name::text) > 10240 then ...
```

In benchmark testing with ~50MB text fields, this change reduced query execution time from ~11 seconds to under 100ms by avoiding full text conversion.

For array columns, implement size limits to prevent excessive data processing:

```sql
case 
  when octet_length(array_column::text) > ${maxSize}
  then (select array_cat(array_column[1:${maxArraySize}]::text[], array['...']))::text[]
  else array_column::text[]
end
```

These techniques are particularly important in data-intensive applications where rendering large text fields or arrays could create bottlenecks.