---
title: Validate database connections explicitly
description: 'Always implement explicit database connection validation strategies
  to ensure robust application behavior during startup and runtime. This includes:


  1. Configure validation queries with appropriate timeouts:'
repository: quarkusio/quarkus
label: Database
language: Java
comments_count: 4
repository_stars: 14667
---

Always implement explicit database connection validation strategies to ensure robust application behavior during startup and runtime. This includes:

1. Configure validation queries with appropriate timeouts:
```properties
quarkus.datasource.jdbc.validation-query-timeout=3
quarkus.datasource.jdbc.validation-query=SELECT 1
quarkus.datasource.jdbc.validate-on-borrow=true
```

2. Control database connectivity during startup:
```properties
# Avoid unnecessary database connections during startup
quarkus.hibernate-orm.database.start-offline=true
```

3. Implement connection validation in critical paths:
```java
@Inject
AgroalDataSource dataSource;

public void validateConnection() throws SQLException {
    try (Connection conn = dataSource.getConnection()) {
        // Execute validation query
        try (Statement stmt = conn.createStatement()) {
            stmt.setQueryTimeout(3);
            stmt.execute("SELECT 1");
        }
    }
}
```

This approach:
- Prevents application failures due to database connectivity issues
- Reduces unnecessary database connections during startup
- Enables proper error handling and recovery
- Improves application reliability in distributed environments

Consider implementing these validations in health checks and critical service initialization points.