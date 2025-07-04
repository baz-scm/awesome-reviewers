---
title: Database-agnostic SQL syntax
description: Write SQL statements that conform to standard SQL rather than relying
  on vendor-specific dialects to ensure portability across different database systems.
repository: spring-projects/spring-framework
label: Database
language: Java
comments_count: 3
repository_stars: 58382
---

Write SQL statements that conform to standard SQL rather than relying on vendor-specific dialects to ensure portability across different database systems.

When working with SQL identifiers (table names, column names, etc.), obtain the appropriate quote characters from the database metadata rather than hardcoding them:

```java
// Get the appropriate quote character for the database
String quoteChar = databaseMetaData.getIdentifierQuoteString();
```

Remember to quote schema and table names independently:

```java
// Correct - Schema and table quoted independently
"INSERT INTO " + quoteChar + "SCHEMA" + quoteChar + "." + quoteChar + "TABLE" + quoteChar

// Incorrect - Combined quoting
"INSERT INTO " + quoteChar + "SCHEMA.TABLE" + quoteChar
```

For database sequences, use standard-compliant syntax:

```java
// Good - standard syntax
"VALUES NEXT VALUE FOR sequence_name"

// Avoid - vendor-specific (Oracle-style)
"select sequence_name.nextval from dual"
```

Some databases like MS SQL Server may have unique quoting requirements or special syntax. Always verify functionality across all target database platforms and avoid compatibility modes or features that are specific to a single database vendor.