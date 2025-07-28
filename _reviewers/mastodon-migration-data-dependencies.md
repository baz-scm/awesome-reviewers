---
title: migration data dependencies
description: Ensure that migrations properly handle data dependencies and sequencing
  to prevent deployment failures. When migrations depend on specific records existing
  (like default roles or seed data), create those records within the migration itself
  rather than relying on seeds or post-deployment processes.
repository: mastodon/mastodon
label: Migrations
language: Ruby
comments_count: 4
repository_stars: 48691
---

Ensure that migrations properly handle data dependencies and sequencing to prevent deployment failures. When migrations depend on specific records existing (like default roles or seed data), create those records within the migration itself rather than relying on seeds or post-deployment processes.

Key considerations:
- **Pre vs Post-deployment timing**: Data deletions and dependency setup should occur in pre-deployment migrations, while column removals and cleanup happen in post-deployment migrations
- **Avoid ActiveRecord models**: Use direct SQL in migrations for better performance and to avoid dependency on model definitions that may change over time
- **Handle missing dependencies**: When adding foreign key constraints or default values that reference other records, ensure those records exist within the same migration

Example from the discussions:
```ruby
class PopulateEveryoneRole < ActiveRecord::Migration[7.1]
  disable_ddl_transaction!
  
  class UserRole < ApplicationRecord
    EVERYONE_ROLE_ID = -99
    FLAGS = { invite_users: (1 << 16) }.freeze
  end
  
  def up
    # Ensure the required role exists before other migrations depend on it
    UserRole.create!(id: UserRole::EVERYONE_ROLE_ID, permissions: UserRole::FLAGS[:invite_users])
  end
end
```

For complex data transformations, consider splitting operations across multiple migrations with proper sequencing, and use `disable_ddl_transaction!` when necessary for large data operations.