---
title: Ensure migration compatibility
description: When modifying database schemas through migrations, ensure compatibility
  with existing data. For new required fields, use `null=True` or provide appropriate
  default values to prevent failures on existing records. Always keep migration files
  synchronized with model changes, and test migrations against a representative dataset
  before deploying to production.
repository: prowler-cloud/prowler
label: Migrations
language: Python
comments_count: 4
repository_stars: 11834
---

When modifying database schemas through migrations, ensure compatibility with existing data. For new required fields, use `null=True` or provide appropriate default values to prevent failures on existing records. Always keep migration files synchronized with model changes, and test migrations against a representative dataset before deploying to production.

For fields added to models that may already have data:
```python
# Good practice:
first_seen_at = models.DateTimeField(null=True, editable=False)
# Or with a default value:
first_seen_at = models.DateTimeField(default=timezone.now, editable=False)

# Problematic - will fail on existing data:
first_seen_at = models.DateTimeField(editable=False)  # No null or default
```

For complex migrations involving raw SQL or custom Python functions, define and test reverse operations (`RunSQL` or `RunPython`). When true reversal is not possible (like adding enum values), use `migrations.RunSQL.noop` to explicitly indicate this limitation. Consider performance impacts when migrations affect large datasets, as this may block application startup.