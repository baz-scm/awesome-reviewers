---
title: Avoid event-loop blocking
description: Do not perform blocking I/O or other long-running synchronous work on
  asyncio’s event loop (especially in async client construction). Offload to worker
  threads (e.g., `asyncio.to_thread`) and prefer lazy credential/platform resolution
  protected by an async lock.
repository: openai/openai-python
label: Concurrency
language: Python
comments_count: 7
repository_stars: 30731
---

Do not perform blocking I/O or other long-running synchronous work on asyncio’s event loop (especially in async client construction). Offload to worker threads (e.g., `asyncio.to_thread`) and prefer lazy credential/platform resolution protected by an async lock.

Also, when canceling/ending streamed responses, ensure you deterministically close the local stream before issuing any remote cancel call, and structure async generator cleanup so sessions/resources are released even if iteration terminates early.

Example pattern (lazy thread offload + guarded resolution):

```python
import asyncio

class AsyncClient:
    def __init__(self, *, use_sigv4: bool):
        self._use_sigv4 = use_sigv4
        self._botocore_credentials = None
        self._creds_lock = asyncio.Lock()

    async def _get_credentials(self):
        if not self._use_sigv4:
            return None
        if self._botocore_credentials is None:
            async with self._creds_lock:
                if self._botocore_credentials is None:
                    # Offload blocking credential lookup/refresh work.
                    self._botocore_credentials = await asyncio.to_thread(_get_default_credentials)
        return self._botocore_credentials

    async def _prepare_request(self, request):
        creds = await self._get_credentials()
        _sign_httpx_request(request, creds, region="us-east-1")
```

Example pattern (stream cancel ordering):

```python
def cancel_stream(stream, cancel_api):
    stream.close()              # close local stream first
    return cancel_api(stream.response_id)
```

Practical checklist:
- Never call code that may hit IMDS/ECS/local filesystem/other blocking APIs from async `__init__` or other event-loop threads.
- Use `asyncio.to_thread` (with appropriate fallback if needed for older Python versions).
- If you must resolve credentials lazily, guard initialization with `asyncio.Lock`.
- For streaming cancel, close/await close before the remote cancel call.
- For async generators/streams, put session/resource cleanup in `finally` (and recognize that if the caller never iterates, your cleanup may not run—design lifecycle accordingly).