---
title: Comprehensive migration planning
description: 'When changing identifier systems (e.g., from using `getInternalId()`
  to `getSequence()`), implement comprehensive migration strategies to preserve data
  integrity and backward compatibility. For each change:'
repository: appwrite/appwrite
label: Migrations
language: PHP
comments_count: 8
repository_stars: 51959
---

When changing identifier systems (e.g., from using `getInternalId()` to `getSequence()`), implement comprehensive migration strategies to preserve data integrity and backward compatibility. For each change:

1. Create explicit migration scripts to update or rename existing resources
2. Implement fallback mechanisms for transitional periods
3. Update all related queries, metrics, and references consistently
4. Test thoroughly with real data before deploying

```php
// Example migration for collection renaming:
public function migrateCollections(): void
{
    $buckets = $this->dbForProject->find('buckets');
    
    foreach ($buckets as $bucket) {
        $oldName = 'bucket_' . $bucket->getInternalId();
        $newName = 'bucket_' . $bucket->getSequence();
        
        if ($this->dbForProject->hasCollection($oldName) && !$this->dbForProject->hasCollection($newName)) {
            // Rename collection to preserve existing data
            $this->dbForProject->renameCollection($oldName, $newName);
            Console::success("Migrated collection {$oldName} → {$newName}");
        }
    }
}
```

Without proper migration planning, changes to identifier systems often result in orphaned data, broken queries, and critical production issues.