---
title: Prevent N+1 database queries
description: Avoid N+1 database queries by using appropriate Django ORM features like
  select_related(), prefetch_related(), and bulk operations. N+1 queries occur when
  you access related objects in a loop, causing additional database queries for each
  iteration.
repository: getsentry/sentry
label: Database
language: Python
comments_count: 5
repository_stars: 41297
---

Avoid N+1 database queries by using appropriate Django ORM features like select_related(), prefetch_related(), and bulk operations. N+1 queries occur when you access related objects in a loop, causing additional database queries for each iteration.

Key practices:
1. Use select_related() for ForeignKey relationships
2. Use prefetch_related() for reverse ForeignKey/ManyToMany relationships
3. Use bulk operations instead of saving in loops

Example - Instead of:
```python
# Creates N+1 queries
for event_type in event_types:
    event_type_snapshot = deepcopy(event_type)
    nullify_id(event_type_snapshot)
    event_type_snapshot.snuba_query = snuba_query_snapshot
    event_type_snapshot.save()
```

Use:
```python
# Single bulk operation
event_type_snapshots = []
for event_type in event_types:
    event_type_snapshot = deepcopy(event_type)
    nullify_id(event_type_snapshot)
    event_type_snapshot.snuba_query = snuba_query_snapshot
    event_type_snapshots.append(event_type_snapshot)
EventType.objects.bulk_create(event_type_snapshots)

# Or for related objects:
team_members = OrganizationMemberTeam.objects.filter(team=team).select_related('organizationmember')
```