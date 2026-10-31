---
title: Async/sync parity and cancellation
description: 'When adding an async counterpart (`acall`, `arun`, `astep`, etc.) to
  an existing sync method (`call`, `run`, `step`), delegate to the same core logic
  instead of re-implementing it. Re-implementations consistently drift: parameters
  get silently dropped (e.g. `current_loop`, `streaming_callback`, `imgs`), retry/model-rotation/bookkeeping
  performed by the sync...'
repository: kyegomez/swarms#pi240310
label: Concurrency
language: Python
comments_count: 8
repository_stars: 7337
---

When adding an async counterpart (`acall`, `arun`, `astep`, etc.) to an existing sync method (`call`, `run`, `step`), delegate to the same core logic instead of re-implementing it. Re-implementations consistently drift: parameters get silently dropped (e.g. `current_loop`, `streaming_callback`, `imgs`), retry/model-rotation/bookkeeping performed by the sync path gets skipped, and special-case branches (streaming, dashboard, error wrapping) that exist in the sync version are missing from the async one. Factor shared pre/post-processing into a helper both paths call, or explicitly document and test which sync behaviors the async path intentionally omits.

```python
# Bad: acall reimplements call(), silently losing retries/bookkeeping/current_loop
async def acall(self, task, current_loop=0, streaming_callback=None, **kwargs):
    return await self.agent.llm.arun(task, **kwargs)  # drops current_loop, streaming_callback

# Good: acall shares call()'s preparation/bookkeeping
async def acall(self, task, current_loop=0, streaming_callback=None, **kwargs):
    run_args = self._prepare_call(task, current_loop, streaming_callback, **kwargs)
    result = await self.agent.llm.arun(**run_args)
    return self._finalize_call(result, current_loop)
```

Additionally, async drivers and task orchestration must respect the asyncio task lifecycle:
- Catch `Exception`, not `BaseException`, in generator drivers/loops that re-throw into coroutines, so `CancelledError`, `KeyboardInterrupt`, and `SystemExit` propagate instead of being swallowed or converted into normal completion.
- When spawning concurrent sub-tasks (`asyncio.ensure_future`, `gather`), cancel and await any still-pending tasks in a `finally` block if the parent coroutine is cancelled, to avoid orphaned tasks mutating shared state after the caller believes the operation finished.
- Validate worker/concurrency-limit inputs before constructing primitives like `asyncio.Semaphore`: treat non-positive values explicitly (e.g. `None`/`<=0` falls back to a safe default) rather than relying on truthiness, which turns `0` into "fallback" but lets a negative value crash or silently produce no concurrency.

```python
# Good: validate before constructing a Semaphore
max_in_flight = (
    self.max_workers
    if self.max_workers is not None and self.max_workers > 0
    else max_workers_95_percent()
)
semaphore = asyncio.Semaphore(max_in_flight)

# Good: cancel and await orphaned tasks on cancellation
try:
    await asyncio.gather(*tasks, return_exceptions=True)
finally:
    for t in tasks:
        if not t.done():
            t.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
```
