---
title: Guard database query results
description: Always validate database query results before accessing their methods
  or properties. Methods like `findOne()`, `getDocument()`, and similar database operations
  can return null or empty documents. Failing to check these results before access
  leads to runtime errors.
repository: appwrite/appwrite
label: Null Handling
language: PHP
comments_count: 3
repository_stars: 51959
---

Always validate database query results before accessing their methods or properties. Methods like `findOne()`, `getDocument()`, and similar database operations can return null or empty documents. Failing to check these results before access leads to runtime errors.

Example of unsafe code:
```php
$latestDeployment = $dbForProject->findOne('deployments', [ /* ... */ ]);
$latestBuild = $dbForProject->getDocument('builds', 
    $latestDeployment->getAttribute('buildId', '')  // May throw if $latestDeployment is null
);
```

Safe pattern:
```php
$latestDeployment = $dbForProject->findOne('deployments', [ /* ... */ ]) 
    ?? new Document();  // Provide empty fallback

if (!$latestDeployment->isEmpty()) {  // Check before accessing
    try {
        $latestBuild = $dbForProject->getDocument(
            'builds',
            $latestDeployment->getAttribute('buildId', '')
        );
    } catch (Throwable $e) {
        $latestBuild = new Document();  // Handle failure gracefully
    }
}
```

Key practices:
1. Provide fallback empty documents when queries may return null
2. Check document existence before accessing properties
3. Use try-catch when chaining dependent queries
4. Consider logging failed lookups in production environments