---
title: True async implementations
description: 'Treat sync and async code paths as first-class, independently correct
  implementations rather than thin wrappers around each other.


  - Never fake async: an `async def` that merely calls a blocking function (`return
  self.run_step(...)`) gives no concurrency benefit and misleads callers. If the underlying
  library offers a true async client/API, use it (see the...'
repository: run-llama/llama_index
label: Concurrency
language: Python
comments_count: 15
repository_stars: 52785
---

Treat sync and async code paths as first-class, independently correct implementations rather than thin wrappers around each other.

- Never fake async: an `async def` that merely calls a blocking function (`return self.run_step(...)`) gives no concurrency benefit and misleads callers. If the underlying library offers a true async client/API, use it (see the Triton/Azure-inference/MySQL examples where sync SDK calls were wrapped in `async def` without actually releasing the event loop). If no async API exists and the work is CPU/IO-bound blocking code that must be exposed asynchronously, explicitly offload it with `asyncio.to_thread(...)` rather than calling it inline.
- Never call `asyncio.run()` (or `nest_asyncio`) from inside a method that may itself be invoked from a running event loop (e.g. a "sync" method called from an async FastAPI handler). This raises `RuntimeError: asyncio.run() cannot be called from a running event loop` or silently breaks nested loops. Instead, implement the async version as the source of truth and have the sync method invoke it through a loop-safe helper, or maintain fully separate sync/async code paths:
  ```python
  # core/async_utils.py provides a loop-safe runner
  from llama_index.core.async_utils import asyncio_run

  def load_data(self, *args, **kwargs):
      return asyncio_run(self.aload_data(*args, **kwargs))

  async def aload_data(self, *args, **kwargs):
      ...
  ```
- Keep sync and async implementations behaviorally mirrored (same validation, same error handling, same return shape) — if one is updated, update the other, and add tests that exercise both.
- Don't close or create async resources (clients, sessions, connectors) from synchronous teardown code with a fresh `asyncio.run()`/event loop; futures/connectors bound to the original loop will raise "attached to a different loop" errors. Expose an explicit `aclose()`/`async with` path for async cleanup and keep `close()` scoped to sync-only resources.
- For fan-out/parallel work (batch calls, multi-page processing, multiple memory blocks, etc.), prefer async concurrency primitives over threads/processes: use `asyncio.gather()` with a semaphore, or the provided `run_jobs(jobs, workers=...)` utility, instead of `ThreadPoolExecutor`/`multiprocessing` for IO-bound operations. When using `asyncio.gather()` over multiple side-effecting operations, track per-task acknowledgements so a partial failure doesn't cause duplicate work on retry.
- Avoid performing network/blocking calls directly in `__init__`; these can't be awaited and make the whole object construction blocking. Prefer lazy initialization triggered on first use (e.g., an `_initialize()` guarded by an `_is_initialized` flag) so construction stays cheap and async-compatible.