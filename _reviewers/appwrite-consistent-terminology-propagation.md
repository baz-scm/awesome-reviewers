---
title: Consistent terminology propagation
description: When changing terminology or naming conventions in a codebase, ensure
  complete and consistent propagation across all related code artifacts. This includes
  variable names, method names, parameters, error messages, documentation, comments,
  and any other references. Inconsistent terminology creates cognitive overhead, leads
  to bugs, and hampers maintainability.
repository: appwrite/appwrite
label: Naming Conventions
language: PHP
comments_count: 15
repository_stars: 51959
---

When changing terminology or naming conventions in a codebase, ensure complete and consistent propagation across all related code artifacts. This includes variable names, method names, parameters, error messages, documentation, comments, and any other references. Inconsistent terminology creates cognitive overhead, leads to bugs, and hampers maintainability.

For example, when transitioning from 'collection' to 'table' terminology:

```diff
// Update method names
- public function testDeleteCollection(array $data)
+ public function testDeleteTable(array $data)

// Update variable names
- $moviesCollectionId = $data['moviesId'];
+ $moviesTableId = $data['moviesId'];

// Update error messages
if (!$dbForProject->deleteDocument('database_' . $db->getInternalId(), $tableId)) {
-    throw new Exception(Exception::GENERAL_SERVER_ERROR, 'Failed to remove collection from DB');
+    throw new Exception(Exception::GENERAL_SERVER_ERROR, 'Failed to remove table from DB');
}

// Update parameter descriptions
-    ->param('name', null, new Text(128), 'Collection name. Max length: 128 chars.')
+    ->param('name', null, new Text(128), 'Table name. Max length: 128 chars.')

// Update event labels
-    ->label('scope', 'collections.write')
+    ->label('scope', 'tables.write')
```

Inconsistent terminology not only confuses developers but can lead to runtime errors when methods or variables with old names are referenced.