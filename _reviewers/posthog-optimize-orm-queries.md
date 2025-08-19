---
title: optimize ORM queries
description: Optimize Django ORM queries to prevent performance issues and unnecessary
  database load. Avoid N+1 query problems by using appropriate prefetch_related()
  and select_related() calls. Remove unnecessary select_related() when you're only
  filtering by foreign key IDs and not accessing the related object. Choose the correct
  database routing (read vs write...
repository: PostHog/posthog
label: Database
language: Python
comments_count: 4
repository_stars: 28460
---

Optimize Django ORM queries to prevent performance issues and unnecessary database load. Avoid N+1 query problems by using appropriate prefetch_related() and select_related() calls. Remove unnecessary select_related() when you're only filtering by foreign key IDs and not accessing the related object. Choose the correct database routing (read vs write replicas) based on the operation. For large tables, prefer database-level filtering over Python-level processing to avoid scanning entire tables.

Example of unnecessary select_related():
```python
# Bad - unnecessary select_related when only filtering by team_id
feature_flag = FeatureFlag.objects.select_related("team").get(key=flag_key, team_id=self._team.id)

# Good - remove select_related when not using the related object
feature_flag = FeatureFlag.objects.get(key=flag_key, team_id=self._team.id)
```

Example of preventing N+1 queries:
```python
# Bad - causes N+1 queries
for obj in Group.objects.all():
    relationship = obj.notebook_relationships.first()

# Good - use prefetch_related to avoid N+1
groups = Group.objects.prefetch_related("notebook_relationships__notebook")
for obj in groups:
    relationship = obj.notebook_relationships.first()
```

For large datasets, use database-level operations instead of scanning entire tables in application code, especially in production environments where tables can be very large.