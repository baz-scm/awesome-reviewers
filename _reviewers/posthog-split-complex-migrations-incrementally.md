---
title: Split complex migrations incrementally
description: Break complex schema changes into multiple, sequential migrations to
  ensure deployment safety and proper data handling. Each migration should represent
  a single, atomic change that can succeed or fail independently.
repository: PostHog/posthog
label: Migrations
language: Python
comments_count: 4
repository_stars: 28460
---

Break complex schema changes into multiple, sequential migrations to ensure deployment safety and proper data handling. Each migration should represent a single, atomic change that can succeed or fail independently.

**Why this matters:**
- Multiple migrations in one PR can cause deployment failures if one succeeds and another fails, leaving the database out of sync with the codebase
- Complex changes are safer when split into logical steps that can be rolled back individually
- Incremental approach allows for safer data migration and validation at each step

**Recommended approach:**
1. **Add nullable field** - Introduce new columns as nullable first
2. **Migrate data** - Populate the new field with appropriate values  
3. **Add constraints** - Apply NOT NULL constraints or other restrictions after data is migrated
4. **Remove old fields** - Deprecate or remove old columns in separate migration

**Example:**
Instead of creating and altering in one migration:
```python
# Avoid: Complex migration doing multiple operations
operations = [
    migrations.AddField(model_name="cohort", name="cohort_type", field=models.CharField(max_length=20, choices=CHOICES)),
    migrations.AlterField(model_name="cohort", name="cohort_type", field=models.CharField(max_length=20, choices=CHOICES, null=False)),
]
```

Prefer incremental steps across separate PRs:
```python
# Step 1: Add nullable field
field=models.CharField(max_length=20, choices=CHOICES, null=True, blank=True)

# Step 2 (separate PR): Migrate existing data
# Step 3 (separate PR): Drop null constraint
```

**One migration per PR** - Keep each PR focused on a single migration to avoid deployment synchronization issues.