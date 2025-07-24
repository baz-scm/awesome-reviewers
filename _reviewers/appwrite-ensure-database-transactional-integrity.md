---
title: Ensure database transactional integrity
description: When performing multiple related database operations, use transactions
  and proper error handling to maintain data consistency. Without proper safeguards,
  partial failures can leave your database in an inconsistent state with orphaned
  or mismatched records.
repository: appwrite/appwrite
label: Database
language: PHP
comments_count: 9
repository_stars: 51959
---

When performing multiple related database operations, use transactions and proper error handling to maintain data consistency. Without proper safeguards, partial failures can leave your database in an inconsistent state with orphaned or mismatched records.

Here are specific practices to follow:

1. **Wrap related operations in transactions** when one operation depends on another:

```php
// BAD: Operations can partially succeed, leaving orphaned metadata
$collection = $dbForProject->createDocument('collections', $metadata);
$dbForProject->createCollection('collection_' . $collection->getInternalId());

// GOOD: Use transaction to ensure atomicity
$dbForProject->withTransaction(function() use ($dbForProject, $metadata) {
    $collection = $dbForProject->createDocument('collections', $metadata);
    $dbForProject->createCollection('collection_' . $collection->getInternalId());
});
```

2. **Add rollback logic** when transactions aren't available:

```php
// GOOD: Explicit rollback when second operation fails
try {
    $collection = $dbForProject->createDocument('collections', $metadata);
    try {
        $dbForProject->createCollection('collection_' . $collection->getInternalId());
    } catch (Exception $e) {
        // Clean up partial state
        $dbForProject->deleteDocument('collections', $collection->getId());
        throw $e;
    }
} catch (Exception $e) {
    // Handle and rethrow
}
```

3. **Return fresh data after mutations** to prevent stale state:

```php
// BAD: Returns stale data
$dbForProject->updateDocument('transactions', $id, ['operations' => $count + 1]);
return $response->dynamic($transaction); // Still has old count!

// GOOD: Return fresh data
$transaction = $dbForProject->updateDocument('transactions', $id, ['operations' => $count + 1]);
return $response->dynamic($transaction); // Has updated count
```

4. **Validate all mutation paths** for operations like bulk creates, updates, increments, and decrements to ensure they're properly processed in transactions.

5. **Use reference capture** (`&$variable`) in database connection factories to properly reuse connections rather than creating new ones on each call.

Implementing these practices will help maintain database integrity, prevent orphaned records, and ensure your application data remains consistent even when operations fail.