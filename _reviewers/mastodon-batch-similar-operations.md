---
title: batch similar operations
description: When performing multiple similar operations (database queries, Redis
  calls, job enqueues, or data lookups), batch them together or eliminate redundancy
  to reduce overhead and improve performance.
repository: mastodon/mastodon
label: Performance Optimization
language: Ruby
comments_count: 5
repository_stars: 48691
---

When performing multiple similar operations (database queries, Redis calls, job enqueues, or data lookups), batch them together or eliminate redundancy to reduce overhead and improve performance.

Common patterns to optimize:
- **Job enqueueing**: Use `perform_bulk` instead of multiple `perform_async` calls
- **Redis operations**: Pipeline multiple Redis commands instead of separate round-trips
- **Data lookups**: Cache or memoize results to avoid repeated parsing/querying
- **Duplicate operations**: Reuse lookup results instead of performing the same operation multiple times

Example transformation:
```ruby
# Before: Multiple individual operations
@domain_block_event.affected_local_accounts.find_each do |account|
  LocalNotificationWorker.perform_async(account.id, event.id, 'AccountRelationshipSeveranceEvent', 'severed_relationships')
end

# After: Batched operations
notification_jobs_args = []
@domain_block_event.affected_local_accounts.find_in_batches do |accounts|
  accounts.each do |account|
    notification_jobs_args.push([account.id, event.id, 'AccountRelationshipSeveranceEvent', 'severed_relationships'])
  end
  LocalNotificationWorker.perform_bulk(notification_jobs_args)
  notification_jobs_args.clear
end
```

This approach reduces network round-trips, memory usage, and processing overhead while maintaining the same functionality.