---
title: Robust aiohttp Networking
description: 'When implementing HTTP/multipart requests and streaming (SSE/chunked)
  parsing with aiohttp, follow these rules:


  - Prefer aiohttp’s built-in primitives for multipart bodies (e.g., MultipartWriter)
  instead of manually encoding file payloads or copying brittle logic from other clients.'
repository: openai/openai-python
label: Networking
language: Python
comments_count: 3
repository_stars: 30731
---

When implementing HTTP/multipart requests and streaming (SSE/chunked) parsing with aiohttp, follow these rules:

- Prefer aiohttp’s built-in primitives for multipart bodies (e.g., MultipartWriter) instead of manually encoding file payloads or copying brittle logic from other clients.
- Manage ClientResponse lifecycle according to aiohttp connection pooling: don’t call close in a way that breaks pooling; ensure the response is released back to the pool (typically via release/reading/using context managers).
- Make streaming parsers robust to transport chunking: never assume chunk boundaries equal line boundaries; split defensively so multiple lines in one chunk and partial lines across chunks are handled.

Example patterns:

```python
# Multipart: use aiohttp primitive rather than ad-hoc dict encoding
writer = aiohttp.MultipartWriter()
# ... append parts to writer ...

# Response lifecycle: release to pool (avoid breaking pooling semantics)
resp = await session.request(...)
try:
    # read/parse as needed
    ...
finally:
    if not resp.closed:
        resp.release()  # return connection to pool

# Streaming parser: be chunk-boundary agnostic
async def parse_stream_async(reader):
    async for chunk in reader:
        for line in chunk.splitlines():
            # handle b"data: " prefix / DONE sentinel as appropriate
            ...
```