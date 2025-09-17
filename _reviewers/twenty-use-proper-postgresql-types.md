---
title: Use proper PostgreSQL types
description: Leverage PostgreSQL's native data types and features instead of generic
  alternatives to improve performance, type safety, and query capabilities. Use JSONB
  for structured data instead of storing raw text, implement PostgreSQL enums for
  constrained values rather than varchar columns, and establish proper foreign key
  relationships with meaningful column names.
repository: twentyhq/twenty
label: Database
language: TypeScript
comments_count: 3
repository_stars: 35477
---

Leverage PostgreSQL's native data types and features instead of generic alternatives to improve performance, type safety, and query capabilities. Use JSONB for structured data instead of storing raw text, implement PostgreSQL enums for constrained values rather than varchar columns, and establish proper foreign key relationships with meaningful column names.

Examples:
- Store structured data as JSONB: `@Column({ type: 'jsonb' })` instead of raw text for better retrieval performance and query capabilities
- Use PostgreSQL enums: `@Column({ type: 'enum', enum: PreferredCalendar })` with database-level enum creation instead of varchar
- Design proper relationships: Use `recordId` and `objectMetadataId` pointing to metadata tables instead of generic `objectId`/`objectType` pairs
- Apply appropriate constraints: Mark columns as non-nullable when they have defaults: `@Column({ nullable: false, default: value })`

This approach enables better query optimization, data integrity, and leverages PostgreSQL's advanced features for improved application performance.