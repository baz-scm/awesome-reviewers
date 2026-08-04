---
title: Enforce Resource Caps
description: For MCP/agent tools, aggressively bound both *inputs* and *outputs* and
  always clean up on timeout/eviction. This prevents runaway memory, long-held locks,
  LLM context blow-ups, and leaked connections / consumed service concurrency.
repository: awslabs/mcp
label: Performance Optimization
language: Python
comments_count: 6
repository_stars: 9545
---

For MCP/agent tools, aggressively bound both *inputs* and *outputs* and always clean up on timeout/eviction. This prevents runaway memory, long-held locks, LLM context blow-ups, and leaked connections / consumed service concurrency.

Apply these rules:
- **Validate numeric parameters at the boundary** (CLI arg parsing / dispatcher). Reject or clamp negatives and enforce documented ranges.
- **Hard-cap result sizes** for any list/scan/pagination and for any “limit” parameter passed into downstream queries.
- **Stop server-side work on timeout** (e.g., Logs Insights queries) so you don’t keep consuming account concurrency after the client gives up.
- **Close resources on eviction** from connection/pool caches (delete from map is not teardown).
- **Cap fan-out** in recursive discovery/analysis (analyzed items must be limited; optionally run bounded parallelism).

Example patterns:

```python
# 1) Clamp user-provided limits at the dispatcher
QUERY_ACTION_MAX_RESULTS_CAP = 200
_SESSION_DETAIL_MAX_LIMIT = 500

def clamp_non_negative_int(x: Any, default: int, cap: int) -> int:
    if x is None:
        return default
    x = int(x)  # let non-numeric raise, or handle explicitly
    if x < 0:
        raise ValueError("must be non-negative")
    return min(x, cap)

# dispatcher
limit = clamp_non_negative_int(limit, default=100, cap=_SESSION_DETAIL_MAX_LIMIT)

# 2) Stop server-side Logs Insights query when polling times out
def run_logs_insights_with_timeout(..., max_poll_seconds: float):
    query_id = logs_client.start_query(...)["queryId"]
    deadline = time.monotonic() + max_poll_seconds
    result = None
    while time.monotonic() < deadline:
        result = logs_client.get_query_results(queryId=query_id)
        if result["status"] in ("Complete", "Failed", "Cancelled"):
            break
        time.sleep(1.0)

    if result is None or result["status"] not in ("Complete", "Failed", "Cancelled"):
        logs_client.stop_query(queryId=query_id)  # crucial cleanup
        return {"status": "Timeout", "queryId": query_id, "results": []}

    return result

# 3) Close cached DB connections/pools when evicting
async def evict_connection(db_connection_map, key, conn):
    db_connection_map.remove_connection(conn)  # delete from map
    await conn.close()  # explicit teardown to avoid leaks
```

Outcome: tools remain predictable under worst-case inputs, stay within service quotas, and won’t degrade performance over time due to leaks or uncontrolled output growth.