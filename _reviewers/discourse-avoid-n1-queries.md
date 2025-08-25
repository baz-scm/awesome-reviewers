---
title: Avoid N+1 queries
description: Prevent N+1 query performance issues by batching database operations
  instead of making individual queries within loops. This is critical for application
  performance as each individual query adds significant overhead.
repository: discourse/discourse
label: Database
language: Ruby
comments_count: 4
repository_stars: 44898
---

Prevent N+1 query performance issues by batching database operations instead of making individual queries within loops. This is critical for application performance as each individual query adds significant overhead.

**Problem Pattern:**
```ruby
# BAD: N+1 queries - one query per iteration
field_ids.map do |fid|
  if UserField.find_by(id: fid).field_type == "confirm"  # Query per field!
    # process field
  end
end

# BAD: N+1 queries in user/group lookups
names.each do |name|
  if user_id = User.find_by_username(name)&.id  # Query per name!
    user_ids << user_id
  elsif group_id = Group.find_by(name: name)&.id  # Query per name!
    group_ids << group_id
  end
end
```

**Solution Pattern:**
```ruby
# GOOD: Single batch query
confirm_field_ids = UserField.where(field_type: "confirm", id: field_ids).pluck(:id)
field_ids.map do |fid|
  if confirm_field_ids.include?(fid)
    # process field
  end
end

# GOOD: Batch queries for users and groups
found_users = User.where(username_lower: names.map(&:downcase)).pluck(:username, :id).to_h
user_ids.concat(found_users.values)
remaining_names = names - found_users.keys
group_ids.concat(Group.where(name: remaining_names).pluck(:id)) if remaining_names.present?
```

Always preload or batch-fetch related data before processing collections. Use `where().pluck()`, `includes()`, or `joins()` to minimize database round trips.