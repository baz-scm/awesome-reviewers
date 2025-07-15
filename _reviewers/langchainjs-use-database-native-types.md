---
title: Use database-native types
description: 'Always leverage database-native data types and appropriate schema design
  to maximize performance and query capabilities. This includes:


  1. Use database-specific type bindings when available instead of generic formats:'
repository: langchain-ai/langchainjs
label: Database
language: TypeScript
comments_count: 4
repository_stars: 15004
---

Always leverage database-native data types and appropriate schema design to maximize performance and query capabilities. This includes:

1. Use database-specific type bindings when available instead of generic formats:
   ```typescript
   // Instead of:
   pref: JSON.stringify(this.pref)
   
   // Prefer:
   pref: { val: JSON.stringify(this.pref), type: oracledb.DB_TYPE_JSON }
   ```

2. For vector stores or cross-platform storage, use serialization-friendly formats for complex types:
   ```typescript
   // Instead of storing Date objects directly
   doc.metadata.date = new Date()
   
   // Store as ISO string for better compatibility
   doc.metadata.date = new Date().toISOString()
   ```

3. In relational databases, prefer specific typed columns over generic JSON fields for data that will be frequently filtered or sorted:
   ```typescript
   // Better schema design with specific columns for important fields
   await engine.pool.raw(`CREATE TABLE ${schemaName}.${tableName}(
     id UUID PRIMARY KEY,
     content TEXT NOT NULL,
     created_date TIMESTAMP NOT NULL,
     category VARCHAR(50) NOT NULL,
     metadata JSON  // Only for truly variable/unstructured data
   )`);
   ```

This approach enables more efficient querying, better indexing capabilities, type validation at the database level, and allows you to leverage database-specific optimizations. Creating typed fields instead of dictionary-style complex types provides better type fidelity and enables richer filtering expressions like numeric/date range comparisons.
