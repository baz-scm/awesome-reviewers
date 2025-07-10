---
title: Migration model imports
description: When writing Django migrations, avoid importing and referencing external
  models directly. Django migrations use auto-generated model classes based on the
  migration state at that point, not the current model definitions. These migration-specific
  models ensure compatibility with the database schema as it existed at that migration's
  point in time.
repository: getsentry/sentry
label: Migrations
language: Python
comments_count: 2
repository_stars: 41297
---

When writing Django migrations, avoid importing and referencing external models directly. Django migrations use auto-generated model classes based on the migration state at that point, not the current model definitions. These migration-specific models ensure compatibility with the database schema as it existed at that migration's point in time.

Instead of importing models directly, use the `apps.get_model()` method provided in migration functions to access the correct version of a model:

```python
# Bad practice:
from sentry.models.organization import Organization

def migrate_data(apps, schema_editor):
    # Wrong: Organization here is the current model, not the migration state model
    orgs = Organization.objects.filter(active=True)
    # ...
```

```python
# Good practice:
def migrate_data(apps, schema_editor):
    # Correct: Gets the Organization model as it exists at migration time
    Organization = apps.get_model("sentry", "Organization")
    orgs = Organization.objects.filter(active=True)
    # ...
```

This approach ensures migrations remain functional even as your models evolve over time, preventing subtle bugs that could corrupt data or break migration sequences.