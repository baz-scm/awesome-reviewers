---
title: Enforce API endpoint consistency
description: 'When implementing or modifying API endpoints, ensure consistency across
  related routes by checking:


  1. Parameter naming matches between route definition and handler:'
repository: appwrite/appwrite
label: API
language: PHP
comments_count: 10
repository_stars: 51959
---

When implementing or modifying API endpoints, ensure consistency across related routes by checking:

1. Parameter naming matches between route definition and handler:
```php
// BAD: Parameter name mismatch
->setHttpPath('/v1/databases/:databaseId/tables/:collectionId/rows')
->action(function(string $databaseId, string $tableId) { ... })

// GOOD: Parameter names align
->setHttpPath('/v1/databases/:databaseId/tables/:tableId/rows')
->action(function(string $databaseId, string $tableId) { ... })
```

2. Response formats are consistent for similar operations:
```php
// BAD: Inconsistent responses for related operations
incrementEndpoint->returns(200, documentModel);
decrementEndpoint->returns(204, noContent);

// GOOD: Consistent response pattern
incrementEndpoint->returns(200, documentModel);
decrementEndpoint->returns(200, documentModel);
```

3. Permission scopes and event names follow the same pattern:
```php
// BAD: Mixed terminology in related endpoints
->label('scope', 'collections.write')
->label('event', 'databases.[databaseId].tables.[tableId].update')

// GOOD: Consistent terminology
->label('scope', 'tables.write')
->label('event', 'databases.[databaseId].tables.[tableId].update')
```

When reviewing API changes, compare against related endpoints to maintain a consistent interface. This helps prevent subtle bugs from parameter mismatches and reduces cognitive load for API consumers.