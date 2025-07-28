---
title: Use asyncio.gather concurrency
description: When performing multiple independent async operations, use `asyncio.gather()`
  to execute them concurrently instead of sequentially. This improves performance
  by allowing operations to run in parallel rather than waiting for each to complete
  before starting the next.
repository: home-assistant/core
label: Concurrency
language: Python
comments_count: 3
repository_stars: 80450
---

When performing multiple independent async operations, use `asyncio.gather()` to execute them concurrently instead of sequentially. This improves performance by allowing operations to run in parallel rather than waiting for each to complete before starting the next.

Apply this pattern when you have:
- Multiple API calls that don't depend on each other
- Independent coordinator refreshes during setup
- Parallel data fetching operations

Avoid creating individual tasks for frequent operations that could be batched together, as this leads to task proliferation and overhead.

Example:
```python
# Instead of sequential execution:
records_a = await client.list_dns_records(zone_id=zone_id, type="A")
records_aaaa = await client.list_dns_records(zone_id=zone_id, type="AAAA")

# Use concurrent execution:
records_a, records_aaaa = await asyncio.gather(
    client.list_dns_records(zone_id=zone_id, type="A"),
    client.list_dns_records(zone_id=zone_id, type="AAAA")
)

# For coordinator setup:
await asyncio.gather(
    *(coordinator.async_config_entry_first_refresh() for coordinator in coordinators)
)
```

This pattern significantly reduces total execution time when operations can run independently and improves overall system responsiveness.