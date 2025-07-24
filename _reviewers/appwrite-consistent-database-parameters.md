---
title: Consistent database parameters
description: 'Maintain consistency and clarity in database-related parameters and
  configuration variables. Follow these practices:


  1. Use descriptive variable names that match parameter names for clarity'
repository: appwrite/appwrite
label: Database
language: Other
comments_count: 2
repository_stars: 51959
---

Maintain consistency and clarity in database-related parameters and configuration variables. Follow these practices:

1. Use descriptive variable names that match parameter names for clarity
2. Follow established naming patterns for database configuration
3. Use 'enabled'/'disabled' instead of boolean values for configuration flags
4. Avoid unnecessary complexity in database parameter handling

**Example 1 - Simplifying parameter handling:**
```php
// Instead of:
$dbService = $this->getParam('database', 'mariadb') === 'mariadb' ? 'mariadb' : 'postgresql';

// Use:
$database = $this->getParam('database', 'mariadb');
```

**Example 2 - Consistent naming for database configuration flags:**
```
// Instead of:
_APP_SLOW_QUERIES=true

// Use:
_APP_SLOW_QUERIES_BLOCK=enabled
```

These practices improve code readability, maintainability, and reduce the potential for errors in database-related code.