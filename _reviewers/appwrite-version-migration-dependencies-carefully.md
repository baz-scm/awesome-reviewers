---
title: Version migration dependencies carefully
description: 'When updating dependencies for migration-related components or making
  schema changes, verify compatibility and ensure backward compatibility:


  1. For dependency updates:'
repository: appwrite/appwrite
label: Migrations
language: Json
comments_count: 3
repository_stars: 51959
---

When updating dependencies for migration-related components or making schema changes, verify compatibility and ensure backward compatibility:

1. For dependency updates:
   - Verify that version constraints point to valid, published versions
   - Check changelogs for breaking API or CLI changes
   - Update lockfiles to lock in the exact tested version
   ```bash
   # After updating a migration dependency in composer.json
   composer update utopia-php/migration && git add composer.lock
   ```

2. For schema changes:
   - Update all affected models, serializers, and tests
   - Ensure systems can handle both old and new schemas during migration periods
   - Test migrations with new dependencies before deployment
   
For example, when adding a new field like `"expired": boolean` to an API schema, update all client models while maintaining compatibility with targets that don't include this field yet.