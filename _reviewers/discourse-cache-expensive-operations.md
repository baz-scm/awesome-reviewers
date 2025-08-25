---
title: Cache expensive operations
description: Identify and eliminate duplicate computations by caching results of expensive
  operations. This includes memoizing method calls, avoiding redundant database queries,
  and caching computed values that are used multiple times.
repository: discourse/discourse
label: Performance Optimization
language: Ruby
comments_count: 3
repository_stars: 44898
---

Identify and eliminate duplicate computations by caching results of expensive operations. This includes memoizing method calls, avoiding redundant database queries, and caching computed values that are used multiple times.

Common patterns to watch for:
- The same method being called multiple times with identical parameters
- Database queries executed repeatedly with the same conditions  
- String interpolations or computations performed for every iteration in loops

Use memoization for expensive operations:
```ruby
def used_flag_ids(flag_ids)
  @used_flag_ids ||= Flag.used_flag_ids(flag_ids)
end
```

Cache intermediate results in loops:
```ruby
# Instead of interpolating keys for every row
records.each { |record| process(interpolate_key(record)) }

# Cache the interpolated keys
cached_keys = records.map { |record| interpolate_key(record) }
cached_keys.each { |key| process(key) }
```

Avoid running the same detection logic multiple times by setting flags or headers to communicate state between components rather than re-computing the same conditions.