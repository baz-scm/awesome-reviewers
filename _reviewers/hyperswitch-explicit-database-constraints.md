---
title: explicit database constraints
description: Be explicit about database constraints and avoid relying on database-level
  defaults. Always specify NOT NULL constraints where appropriate and let the application
  layer handle default values rather than the database schema. Use appropriate primary
  key strategies like SERIAL for auto-incrementing IDs.
repository: juspay/hyperswitch
label: Database
language: Sql
comments_count: 2
repository_stars: 34028
---

Be explicit about database constraints and avoid relying on database-level defaults. Always specify NOT NULL constraints where appropriate and let the application layer handle default values rather than the database schema. Use appropriate primary key strategies like SERIAL for auto-incrementing IDs.

This approach gives the application more control over data validation and ensures schema intentions are clear to all developers.

Example:
```sql
-- Avoid this - implicit nullability and database defaults
CREATE TABLE user_session (
    id VARCHAR(64) PRIMARY KEY,
    created_at TIMESTAMP DEFAULT now()
);

-- Prefer this - explicit constraints and application-controlled defaults  
CREATE TABLE user_session (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(128) NOT NULL,
    created_at TIMESTAMP NOT NULL
);
```