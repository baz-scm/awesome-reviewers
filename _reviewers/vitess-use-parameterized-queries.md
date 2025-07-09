---
title: Use parameterized queries
description: Always use parameterized queries with bind variables instead of string
  concatenation or formatting when constructing SQL statements. This prevents SQL
  injection attacks and improves query performance through better statement caching.
repository: vitessio/vitess
label: Database
language: Go
comments_count: 4
repository_stars: 19815
---

Always use parameterized queries with bind variables instead of string concatenation or formatting when constructing SQL statements. This prevents SQL injection attacks and improves query performance through better statement caching.

**Instead of this:**
```go
query := `SELECT variable_value FROM performance_schema.global_status WHERE variable_name IN (`
for _, status := range statuses {
    query += `"` + status + `"`
}
query += ");"
qr, err := mysqld.FetchSuperQuery(ctx, query)
```

**Do this:**
```go
statusBv, err := sqltypes.BuildBindVariable(statuses)
if err != nil {
    return nil, err
}
query, err := sqlparser.ParseAndBind(
    "SELECT variable_name, variable_value FROM performance_schema.global_status WHERE variable_name IN %a",
    statusBv,
)
if err != nil {
    return nil, err
}
qr, err := mysqld.FetchQuery(ctx, query)
```

When building dynamic SQL statements, especially those with user-provided input, always use the SQL parser and bind variables. This approach not only prevents SQL injection but also allows the database to cache and reuse execution plans, improving performance for frequently executed queries with different parameter values.