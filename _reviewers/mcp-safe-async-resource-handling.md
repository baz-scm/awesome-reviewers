---
title: Safe Async Resource Handling
description: 'Shared resources (connections, clients, caches) must be concurrency-safe
  across async tool invocations.


  **Standard**

  1. **Validate before publish**: never put a resource into a shared cache/map until
  it is known-good. This prevents race windows where other coroutines can use an unvalidated
  handle.'
repository: awslabs/mcp
label: Concurrency
language: Python
comments_count: 7
repository_stars: 9545
---

Shared resources (connections, clients, caches) must be concurrency-safe across async tool invocations.

**Standard**
1. **Validate before publish**: never put a resource into a shared cache/map until it is known-good. This prevents race windows where other coroutines can use an unvalidated handle.
2. **Do not block the event loop or hold locks during long I/O**:
   - Offload synchronous/blocking calls with `await asyncio.to_thread(...)` / `run_in_executor`.
   - If a lock guards reconnection/cleanup, ensure the connect/handshake/auth path has its own bounded timeout (separate from query/operation timeouts).
3. **Reliable cleanup on shutdown/cancellation**:
   - If you schedule async cleanup with `create_task`, you must either **await/drain** it (or guarantee the loop won’t stop before it runs) or **log** which resources were scheduled and why they may not complete.
   - Avoid trying to close async-loop-bound resources using `asyncio.run()` from the wrong loop; prefer clearing/discarding pools when loop ownership would conflict.
4. **Synchronize shared mutable state**:
   - For module-level caches/indexes rebuilt in async flows, use an `asyncio.Lock` and perform an atomic swap of the fully built data so readers never observe partial state.
   - For request-scoped overrides (region, client factory), use `contextvars` (or otherwise ensure no process-global mutation without isolation).

**Practical patterns**
- **Validate-then-set** (eliminates orphan windows):
```py
# BAD: cache-before-validate
map[key] = conn
conn.validate()  # another coroutine may grab conn while invalid

# GOOD: validate first, then publish
conn.validate()
with lock:
    map[key] = conn
```
- **Offload blocking work**:
```py
# In async tool
result = await asyncio.to_thread(sync_fn, *args)
```
- **Bound connection/handshake even if query timeout exists**:
```py
options = {SQL_ATTR_LOGIN_TIMEOUT: login_timeout_s}
# so reconnect can't hold a lock for OS TCP/TLS timeouts
```
- **Shutdown cleanup diagnostics**:
```py
# If loop may be stopping, log scheduling info and/or drain tasks.
for key, conn in snapshot:
    coro = conn.close()
    if isawaitable(coro):
        tasks.append(asyncio.create_task(coro))
        logger.warning(f"Scheduled close for {key}")
# Prefer: await asyncio.gather(*tasks, return_exceptions=True)
```

If you adopt these rules for every shared connection/client/cache and every async entrypoint, you eliminate the majority of concurrency defects shown in the discussions: race windows, lock starvation, event-loop pinning, silent leaks, and partially built shared state.