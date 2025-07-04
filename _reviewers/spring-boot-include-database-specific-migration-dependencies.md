---
title: Include database-specific migration dependencies
description: When implementing database migrations with tools like Flyway, ensure
  you include the appropriate database-specific dependency for your target database.
  As of Flyway V10.0.0, all databases except in-memory or file-based ones (such as
  H2 or SQLite) require their own specific dependency package.
repository: spring-projects/spring-boot
label: Migrations
language: Other
comments_count: 2
repository_stars: 77637
---

When implementing database migrations with tools like Flyway, ensure you include the appropriate database-specific dependency for your target database. As of Flyway V10.0.0, all databases except in-memory or file-based ones (such as H2 or SQLite) require their own specific dependency package.

For example:
- For PostgreSQL: `org.flywaydb:flyway-database-postgresql`
- For MySQL: `org.flywaydb:flyway-mysql`

Note that not all database modules follow the same naming pattern. Always consult the official documentation (https://documentation.red-gate.com/flyway/flyway-cli-and-api/supported-databases) for the most current information about required dependencies for your specific database platform.

Including the correct database-specific dependency is essential for successful schema migrations and prevents runtime errors when your application attempts to initialize the database.