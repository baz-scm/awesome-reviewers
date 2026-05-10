---
title: Non-Blocking Async Recovery
description: 'Concurrency standard: (1) keep async code non-blocking, (2) don’t change
  sync/async boundaries unless callers support it, and (3) make recovery/state transitions
  race-safe.'
repository: infiniflow/ragflow
label: Concurrency
language: Python
comments_count: 6
repository_stars: 80174
---

Concurrency standard: (1) keep async code non-blocking, (2) don’t change sync/async boundaries unless callers support it, and (3) make recovery/state transitions race-safe.

**Rules**
1) **Never call blocking (sync) work from async tasks**. If you must use a sync API (e.g., `llm.chat()`), offload it (or refactor to an async client).
2) **Match sync/async signatures to callers**. If a function is only called from sync code, keep it sync (don’t make it `async` just to “fit”); if callers are async, then the callee can be async.
3) **Recovery/requeue logic must avoid TOCTOU**. When detecting “orphaned” or incomplete tasks, use an atomic snapshot, transaction, or a re-check/lock so you don’t incorrectly downgrade DONE → FAIL.
4) **For time-sensitive heartbeat/recovery, avoid blocking the event loop**. If Redis operations or other work are blocking, run them in a dedicated worker thread/process or ensure the client calls are truly non-blocking.
5) **Use explicit stop coordination for graceful shutdown** (e.g., stop_event set by SIGTERM/SIGINT) so recovery loops exit cleanly.

**Example: offload sync call from async**
```python
import asyncio

async def chat_async(chat_model, system_msg, hist, conf):
    # chat_model.chat is sync; offload so the event loop stays responsive
    response = await asyncio.to_thread(chat_model.chat, system_msg, hist, conf)
    return response
```

**Example: avoid TOCTOU in requeue**
- Perform the “orphaned docs” lookup and “incomplete tasks” lookup under a consistent transaction, or
- Re-check document/task state right before updating, and only mark FAIL if the state still indicates “no incomplete tasks.”

Applying these rules prevents event-loop stalls, fixes incorrect concurrency boundaries, and eliminates correctness bugs during crash recovery and task requeue.