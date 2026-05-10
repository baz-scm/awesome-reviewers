---
title: Avoid shared mutable state
description: 'When working with concurrency (threads/async), ensure code is safe under
  parallel invocations and does not block or re-enter running event loops.


  Rules:'
repository: langchain-ai/langchain
label: Concurrency
language: Python
comments_count: 9
repository_stars: 136312
---

When working with concurrency (threads/async), ensure code is safe under parallel invocations and does not block or re-enter running event loops.

Rules:
1) Eliminate shared mutable state across requests/threads
- Prefer immutable middleware/config objects.
- Never store request-specific data in process-global or shared containers unless it is explicitly per-thread/per-run.

2) Be event-loop safe
- Never call `asyncio.run()`/`loop.run_until_complete()` when a loop may already be running.
- Provide real async APIs for IO-bound work; for sync entrypoints, delegate blocking work to an executor.

3) Provide and test async behavior
- If production uses async, add unit tests for async paths.
- Add coverage for parallel execution (e.g., parallel tool calls).

4) Keep async detection consistent
- Prefer `inspect.iscoroutinefunction` over `asyncio.iscoroutinefunction` for newer Python/mypy compatibility.

Example patterns:
```python
# 1) Immutability / no post-init mutation
class ConditionalModelSettingsMiddleware(AgentMiddleware):
    def __init__(self, conditions: list[tuple[Callable, dict[str, Any]]]):
        super().__init__()
        self._conditions = list(conditions)  # don’t mutate after init
```
```python
# 2) Offload blocking work from async contexts
async def abefore_agent(self, state, runtime):
    return await run_in_executor(None, self.before_agent, state, runtime)
```
```python
# 3) Don’t use asyncio.run() inside possibly-running event loops
# Prefer: make the validation async, or detect running loop and schedule appropriately.
async def _avalidate(...):
    ...
# then in async contexts: await _avalidate(...)
```
```python
# 4) Prefer inspect for coroutine-function checks
import inspect
if ignore_condition_name is None or not getattr(handler, ignore_condition_name):
    event = getattr(handler, event_name)
    if inspect.iscoroutinefunction(event):
        ...
```

Adopting these practices prevents race conditions, avoids event-loop reentrancy problems, and ensures concurrency-heavy logic is correct under real async/parallel workloads.