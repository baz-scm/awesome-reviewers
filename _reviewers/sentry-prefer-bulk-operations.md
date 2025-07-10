---
title: Prefer bulk operations
description: 'When implementing functionality that processes multiple items, always
  consider the performance implications of individual versus batch processing. Avoid
  fetching or processing items one-by-one in loops, as this can lead to significant
  performance degradation, especially at scale. Instead:'
repository: getsentry/sentry
label: Performance Optimization
language: Python
comments_count: 3
repository_stars: 41297
---

When implementing functionality that processes multiple items, always consider the performance implications of individual versus batch processing. Avoid fetching or processing items one-by-one in loops, as this can lead to significant performance degradation, especially at scale. Instead:

1. Use bulk database queries or APIs when available
2. Consider implementing batching for operations that must be done individually
3. Use threadpools for parallelization when appropriate
4. Place cache lookups before expensive operations to avoid unnecessary processing
5. Implement pagination with reasonable page sizes for large datasets

Example - Problematic:
```python
# Performance issue: Individual queries in a loop
def fetch_error_details(project_id: int, error_ids: list[str]) -> list[dict[str, Any]]:
    error_details = []
    for error_id in error_ids:
        try:
            event = eventstore.get_event_by_id(project_id, error_id)  # Separate query for each ID
            # Process event...
        # ...
    return error_details
```

Example - Improved:
```python
# Better: Single bulk query
def fetch_error_details(project_id: int, error_ids: list[str]) -> list[dict[str, Any]]:
    if not error_ids:
        return []
    # Use a bulk query instead of individual queries
    events = eventstore.get_events_by_ids(project_id, error_ids)
    # Process events...
    return error_details
```

This pattern applies to any situation where you might be tempted to make repeated database calls, API requests, or process large amounts of data item-by-item. Bulk operations significantly reduce overhead, network latency, and processing time.