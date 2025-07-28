---
title: context-independent schema design
description: Database schema elements (views, constraints, tables) should be designed
  to be context-independent and self-contained. This means all identifiers should
  be fully qualified, and only information supported by the SQL parser should be included
  in DDL representations.
repository: apache/spark
label: Database
language: Java
comments_count: 3
repository_stars: 41554
---

Database schema elements (views, constraints, tables) should be designed to be context-independent and self-contained. This means all identifiers should be fully qualified, and only information supported by the SQL parser should be included in DDL representations.

Key principles:
1. **Fully qualify identifiers**: View text should contain fully qualified identifiers (catalog.schema.table) to avoid dependency on current context
2. **Parser-compatible DDL**: Only include information in DDL output that is supported by the SQL parser - remove unsupported elements like validation status
3. **Self-contained definitions**: Schema elements should not rely on external context like current catalog or namespace

Example of context-independent view text:
```java
// Bad - context-dependent
"SELECT * FROM my_table"

// Good - context-independent  
"SELECT * FROM my_catalog.my_schema.my_table"
```

Example of parser-compatible constraint DDL:
```java
// Remove unsupported validation status from DDL
return String.format(
    "CONSTRAINT %s %s %s %s",
    name,
    definition(),
    enforced ? "ENFORCED" : "NOT ENFORCED"
    // validationStatus removed - not supported by parser
);
```

This approach ensures schema portability, reduces ambiguity, and maintains compatibility with SQL standards.