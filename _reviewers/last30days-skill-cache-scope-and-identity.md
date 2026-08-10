---
title: Cache Scope And Identity
description: 'Ensure caching is both lifecycle-correct and identity-safe.


  - Lifecycle: Cache invalidation/reset must match the intended scope (e.g., “run”
  not “process”). If long-lived workers exist, reset at deterministic pipeline boundaries
  (e.g., external pipeline entry) and not in internal sub-runs.'
repository: mvanhorn/last30days-skill
label: Caching
language: Python
comments_count: 2
repository_stars: 57799
---

Ensure caching is both lifecycle-correct and identity-safe.

- Lifecycle: Cache invalidation/reset must match the intended scope (e.g., “run” not “process”). If long-lived workers exist, reset at deterministic pipeline boundaries (e.g., external pipeline entry) and not in internal sub-runs.
- Cache keys: Include every parameter dimension that changes the fetched result (e.g., topic normalization, depth/count, date range).
- Identity-safe rehydration: When refetching using cached items, verify the remote response corresponds to the same entity. If you have a real numeric ID, require the refetch result to match that ID (even when using slug fallback). If identity is synthetic/unknown, skip the strict check but avoid making strong claims.

Example pattern (lifecycle + identity check):
```python
# lifecycle reset at correct boundary
if not internal_subrun:
    reset_search_cache()  # run-scoped invalidation

# key must cover all query dimensions
cache_key = (core_topic, count, from_date)

# identity-safe refetch
def refetch_datum(item, datum_key):
    event_id = str(getattr(item, "metadata", {}).get("event_id") or "").strip()
    slug = extract_slug(item.url)  # parse from URL

    payload = http_request_lookup(event_id or slug)

    if event_id:
        # If we used slug fallback, still enforce ID match
        chosen = pick_matching_event(payload, expected_event_id=event_id)
        if chosen is None:
            raise ValueError("Event identity mismatch; degrade safely")
    return payload
```

This prevents stale cross-run reuse (wrong cache lifetime) and prevents cross-entity contamination (wrong identity during refetch), both of which lead to incorrect cached results.