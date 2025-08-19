---
title: Cache expensive operations
description: Identify and eliminate redundant expensive operations by implementing
  caching, memoization, or conditional execution. Look for repeated database queries,
  complex calculations, object creation, or data processing that can be cached or
  avoided entirely when not needed.
repository: PostHog/posthog
label: Performance Optimization
language: Python
comments_count: 5
repository_stars: 28460
---

Identify and eliminate redundant expensive operations by implementing caching, memoization, or conditional execution. Look for repeated database queries, complex calculations, object creation, or data processing that can be cached or avoided entirely when not needed.

Common patterns to optimize:
- **Repeated database queries**: Extract common query logic and cache results
- **Expensive lookups**: Cache lookup results to avoid O(n²) complexity when searching through collections multiple times
- **Conditional expensive operations**: Skip unnecessary work when results won't be used (e.g., timing calculations when debug mode is off)
- **Object recreation**: Cache expensive-to-create objects like compiled regex patterns or metric meters

Example of query optimization:
```python
# Before: Duplicated query logic
if cache_enabled:
    tables = list(
        DataWarehouseTable.objects.filter(team_id=team.pk)
        .exclude(deleted=True)
        .select_related("credential", "external_data_source")
        .fetch_cached(team_id=team_id or team.pk, key_prefix=CACHE_KEY_PREFIX)
    )
else:
    tables = list(
        DataWarehouseTable.objects.filter(team_id=team.pk)
        .exclude(deleted=True)
        .select_related("credential", "external_data_source")
    )

# After: Extract common logic, apply caching conditionally
tables = DataWarehouseTable.objects.filter(team_id=team.pk)
    .exclude(deleted=True)
    .select_related("credential", "external_data_source")
if cache_enabled:
    tables = tables.fetch_cached(team_id=team_id or team.pk, key_prefix=CACHE_KEY_PREFIX)
```

Example of lookup caching:
```python
# Add caching to avoid O(n²) complexity
def _get_all_loaded_insight_ids(self) -> set[int]:
    """Get all insight IDs from loaded pages."""
    if not hasattr(self, '_cached_insight_ids'):
        all_ids = set()
        for page_insights in self._loaded_pages.values():
            for insight in page_insights:
                all_ids.add(insight.id)
        self._cached_insight_ids = all_ids
    return self._cached_insight_ids
```