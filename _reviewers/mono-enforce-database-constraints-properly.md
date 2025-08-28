---
title: enforce database constraints properly
description: Database schemas should use appropriate constraints to enforce business
  rules and prevent data inconsistencies. When designing tables, identify potential
  duplicate data scenarios and implement unique constraints to prevent them. Consider
  consolidating related tables when a single table with proper constraints can achieve
  the same goal more efficiently.
repository: rocicorp/mono
label: Database
language: Sql
comments_count: 3
repository_stars: 2091
---

Database schemas should use appropriate constraints to enforce business rules and prevent data inconsistencies. When designing tables, identify potential duplicate data scenarios and implement unique constraints to prevent them. Consider consolidating related tables when a single table with proper constraints can achieve the same goal more efficiently.

For example, instead of allowing duplicate emoji assignments:
```sql
-- Problem: Allows same user to assign same emoji multiple times
CREATE TABLE emoji (
    "id" VARCHAR PRIMARY KEY,
    "value" VARCHAR NOT NULL,
    "subjectID" VARCHAR NOT NULL,
    "creatorID" VARCHAR REFERENCES "user"(id)
);

-- Solution: Add unique constraint to prevent duplicates
CREATE TABLE emoji (
    "id" VARCHAR PRIMARY KEY,
    "value" VARCHAR NOT NULL,
    "subjectID" VARCHAR NOT NULL,
    "creatorID" VARCHAR REFERENCES "user"(id),
    UNIQUE ("subjectID", "creatorID", "value")
);
```

Additionally, document non-obvious schema design decisions with comments, especially when columns might seem redundant but serve specific business logic purposes. Consider primary key ordering based on common query patterns - place the most frequently filtered column first for better performance.