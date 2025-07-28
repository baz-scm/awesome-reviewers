---
title: Optimize database queries
description: 'Write efficient database queries by leveraging proper indexes, using
  performance-optimized ActiveRecord methods, and avoiding unnecessary database operations.
  Key practices include:'
repository: mastodon/mastodon
label: Database
language: Ruby
comments_count: 5
repository_stars: 48691
---

Write efficient database queries by leveraging proper indexes, using performance-optimized ActiveRecord methods, and avoiding unnecessary database operations. Key practices include:

1. **Use indexes effectively**: Structure queries to utilize existing indexes. For example, use `Account.arel_table[:username].lower.in(usernames.map(&:downcase))` to leverage lowered username indexes instead of queries that cause sequential scans.

2. **Prefer exists() over count()**: Use `exists?` instead of `count.zero?` to avoid unnecessary COUNT operations:
```ruby
# Instead of
Follow.where(conditions).count.zero?

# Use
!Follow.where(conditions).exists?
```

3. **Remove redundant indexes**: Avoid creating single-column indexes when composite indexes already cover them. An index on `["account_id", "group_id"]` makes a separate `["account_id"]` index unnecessary.

4. **Simplify complex queries**: When Arel becomes overly complex, consider raw SQL for better readability and maintainability:
```ruby
# Instead of complex Arel constructions
scope :matches_partially, ->(str) { where("'%' || username || '%'") }
```

5. **Handle query ordering conflicts**: Use `reorder(nil)` to clear existing ORDER BY clauses when they conflict with new ordering requirements, preventing incorrect results from multiple conflicting sort orders.