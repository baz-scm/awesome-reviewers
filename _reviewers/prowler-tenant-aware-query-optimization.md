---
title: Tenant-aware query optimization
description: Always include tenant_id filters in database queries for multi-tenant
  systems to maintain data isolation and improve query performance. In ORM queries,
  explicitly filter by tenant_id even when using Row Level Security (RLS) as a defense-in-depth
  measure and to help the query optimizer.
repository: prowler-cloud/prowler
label: Database
language: Python
comments_count: 3
repository_stars: 11834
---

Always include tenant_id filters in database queries for multi-tenant systems to maintain data isolation and improve query performance. In ORM queries, explicitly filter by tenant_id even when using Row Level Security (RLS) as a defense-in-depth measure and to help the query optimizer.

When fetching data in multi-tenant contexts:

```python
# AVOID: Missing tenant filter can leak data across tenants
return LighthouseConfig.objects.all()

# RECOMMENDED: Always filter by tenant_id 
return LighthouseConfig.objects.filter(tenant_id=self.request.tenant_id)
```

Additionally, optimize database access by:
1. Consolidating related queries to reduce round trips
2. Caching results when appropriate
3. Moving logic to avoid redundant queries for the same data

Example of optimizing repeated queries:
```python
# AVOID: Extra query when delta is not NEW
if delta != Finding.DeltaChoices.NEW:
    first_seen = (
        Finding.objects.filter(uid=finding_uid, delta=Finding.DeltaChoices.NEW.value)
        .values("first_seen")
        .first()["first_seen"]
    )

# RECOMMENDED: Retrieve first_seen during delta calculation to avoid extra query
# In _create_finding_delta function:
def _create_finding_delta(last_status, current_status, last_finding=None):
    # Calculate delta...
    first_seen = datetime.now(tz=timezone.utc)
    if delta != Finding.DeltaChoices.NEW and last_finding:
        first_seen = last_finding.first_seen
    return delta, first_seen
```