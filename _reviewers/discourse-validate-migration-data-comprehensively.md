---
title: validate migration data comprehensively
description: Migration scripts must thoroughly validate data conditions and handle
  edge cases to ensure reliable data transformation. Always check for data existence
  before applying operations, properly handle duplicate records, and avoid migrating
  calculated or derived fields.
repository: discourse/discourse
label: Migrations
language: Ruby
comments_count: 5
repository_stars: 44898
---

Migration scripts must thoroughly validate data conditions and handle edge cases to ensure reliable data transformation. Always check for data existence before applying operations, properly handle duplicate records, and avoid migrating calculated or derived fields.

Key practices:
- **Check data existence**: Verify that related data exists before performing operations (e.g., "Should we update that site setting only when there are tag groups?")
- **Handle duplicates gracefully**: Ensure migrations can continue when duplicates are found, returning existing records rather than failing
- **Skip calculated fields**: Exclude computed columns like `first_unread_pm_at` that should be recalculated rather than migrated
- **Cover edge cases**: Consider scenarios like missing seed data or schema evolution (e.g., custom palettes based on non-seeded built-in schemes)
- **Manage schema changes**: When fields are split or renamed, maintain backward compatibility and proper synchronization

Example of proper duplicate handling:
```ruby
duplicate = DB.query_single(<<~SQL, name: name).first
  SELECT id from ai_personas where name = :name
SQL

if duplicate.present?
  duplicate  # Return existing record to continue migration
else
  # Create new record
end
```

This approach prevents migration failures and ensures data integrity across different migration scenarios and schema versions.